Geo Point with Elasticsearch 2.x
================================
:desc: Getting geo coordinates into elasticsearch 2
:date: 2015-12-22
:tags: elasticsearch, kibana, logstash, geo

I was recently brought into an interesting project that deals with analyzing
some exciting data. I have my preferred search solutions and hate java, but
I had to bite my tongue and acknowledge an ELK stack is the best tool for this
particular job.

ELK Stack
---------

An "ELK stack" refers to logstash, elasticsearch, and kibana. It's worth noting
that one should always ensure the versions they use match up on the compatibility
matrix.

Back in the kibana 3 days, things were pretty magical. There was less integration
with elasticsearch and kibana was mostly left up to guess what was in elasticsearch.

Kibana 4
--------

Kibana 4 has significantly more features and more integration with elasticsearch,
but it means a lot of added complexity. The number one headache I faced was
putting a geo\_point into elasticsearch so that kibana 4 could plot it. I had the
geo coordinates, so it seemed like sticking it into a geo\_point field should be
absolutely trivial.

Unfortunately, you can't just tell logstash that these coordinates are
geographical coordinates. That's because logstash will speak JSON and geo\_point
is not a valid type.

ELK and geo\_point
------------------

In order to get our coordinates from logstash to a kibana 4 map, we have two
options. Our first option is to issue a curl request against elasticsearch that
will modify the index. In my opinion, this is a sub-par option. The other option
is to generate a new template to be used on a new index that includes the
coordinates. This means doing everything within logstash.

Logstash Template
-----------------

The default template for any elasticsearch index matching "logstash-\*" is
"elasticsearch-template.json" and it's location depends on how you chose to
install logstash.

It's contents will look like this:

.. code-block:: json

    {
      "template": "logstash-*",
      "settings": {
        "index.refresh_interval": "5s"
      },
      "mappings": {
        "_default_": {
           "_all": {"enabled": true, "omit_norms": true},
           "dynamic_templates": [ {
             "message_field": {
               "match": "message",
               "match_mapping_type": "string",
               "mapping": {
                 "type": "string", "index": "analyzed", "omit_norms": true
               }
             }
           }, {
             "string_fields": {
               "match": "*",
               "match_mapping_type": "string",
               "mapping": {
                 "type": "string", "index": "analyzed", "omit_norms": true,
                   "fields": {
                     "raw": {"type": "string", "index": "not_analyzed", "ignore_above": 256}
                   }
               }
             }
           } ],
           "properties": {
             "@version": { "type": "string", "index": "not_analyzed" },
             "geoip"  : {
               "type": "object",
                 "dynamic": true,
                 "properties": {
                   "location": { "type": "geo_point" }
                 }
             }
           }
        }
      }
    }

This geoip field is for if we're providing an IP address that we want processed
and turned into geographical coordinates. In our scenario, we already have this
data, so this field is useless. However, we do need a geo\_point field.

Let's create /etc/logstash/templates/monster.json:

.. code-block:: json

    {
      "template": "monster-*",
      "settings": {
        "index.refresh_interval": "60s"
      },
      "mappings": {
        "_default_": {
          "_all": {"enabled": true, "omit_norms": true},
          "dynamic_templates": [ {
            "message_field": {
              "match": "message",
              "match_mapping_type": "string",
              "mapping": {
                "type": "string", "index": "analyzed", "omit_norms": true
              }
            }
          }, {
            "string_fields": {
              "match": "*",
              "match_mapping_type": "string",
              "mapping": {
                "type": "string", "index": "analyzed", "omit_norms": true,
                "fields": {
                  "raw": {"type": "string", "index": "not_analyzed", "ignore_above": 256}
                }
              }
            }
          } ],
          "properties": {
            "@version": { "type": "string", "index": "not_analyzed" },
            "lonlat": { "type": "geo_point" }
          }
        }
      }
    }

What changed:

* Template name changed
* The geoip object was removed
* The lonlat field was added

Logstash Configuration
----------------------

Everything in logstash is driven by the configuration files. These are usually
located in /etc/logstash/conf.d/<filename>.conf.

To get this working, we need to ensure that the lonlat field is populated and we
need to make sure the output uses the correct index name and template.

The filter { } section is relatively simple. In my case, I had the data, but the
longitude and latitude fields were flipped.

My filter section of /etc/logstash/conf.d/monster.json:

.. code-block:: text

    filter {
      # Monster Attacks
      if [type] == "monster_data" {
        # [...]
        if [monster_location] {
          grok {
            match => [ "monster_location", "%{BASE10NUM:latitude:float},%{BASE10NUM:longitude:float}" ]
          }
          mutate {
            add_field => [ "[lonlat]", "%{longitude}" ]
            add_field => [ "[lonlat]", "%{latitude}" ]
          }
        }
      }
    }

The next thing we need is an output to elasticsearch that pulls all of these
modifications together.

.. code-block:: text

    output {
      if [type] == "monster_data" {
        # Send to elasticsearch set hosts entry to the IP of your elasticsearch node
        elasticsearch {
          template => "/etc/logstash/templates/monster.json"
          template_overwrite => true
          hosts => "127.0.0.1:9200"
          workers => "2"
          index =>  "monster-%{+YYYY.MM.dd}"
        }
      }
    }

This is an output to elasticsearch that uses our custom template.

Summary
-------

Now, feel free to start ingesting data. When you try to plot these points on a
map within Kibana 4, you'll be able to use the lonlat field that we created.

Overall, this is actually a *very* simple thing to do. It's just been documented
very poorly. I hope that this helps others learn about storing a geo\_point field
as well as working with logstash templates. :)
