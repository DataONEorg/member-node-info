# Member Node Custom Properties

Member Nodes generally control the content available in the Member Node document provided through the [/node](https://cn.dataone.org/cn/v2/node) service. This document describes custom properties that may be set by the Coordinating Nodes to augment the information provided by the Member Nodes. Such custom properties are not over-written by a Member Node when the Member Node registration information is updated.

Custom properties set by the Coordinating Nodes MUST be prefixed by `CN_`. Such properties will be preserved through updates to the node registration. Note that the string "CN_" has no meaning other than to act as a mechanism for distinguishing custom properties from other properties that may be set by the MN.

The value of the custom property `${PROPERTY}` for the Member Node `${NODE_ID}` can be determined from the DataONE [list nodes API](https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html#CNCore.listNodes) with the following XPath statement:

```
//node[identifier/text()='${NODE_ID}']/property[@key='${PROPERTY}']
```

For example, using `curl` and `xmlstarlet`:

```bash
NODE_ID="urn:node:KNB"
PROPERTY="CN_date_operational"
curl -s "https://cn.dataone.org/cn/v2/node" | \
  xml sel -t \
  -m "//node[identifier/text()='${NODE_ID}']/property[@key='${PROPERTY}']" -v "."
2012-07-23T00:00:0.000Z
```

## Preferred Custom Properties

The following custom properties are used by systems such as the DataONE [search interface](https://search.dataone.org) and [Member Node dashboard](https://www.dataone.org/current-member-nodes).

For properties that express a date, these MUST be in UTC and formatted as ISO-8601 (`YYYY-MM-DDTHH:mm:ss.sssZ`). If the time portion is unknown, then substitute `00:00:00.000`. Example:

```
2017-03-20T15:25:53.514Z
```


### `CN_node_name`

Provides the same information as the [`name`](https://releases.dataone.org/online/api-documentation-v2.0/apis/Types.html#Types.Node.name) element of the node document though may optionally be augmented by DataONE to provide additional or clarifying details.

Example:

```xml
<property key="CN_node_name">node name text string</property>
```


### `CN_operational_status`

Indicates the current operational status of the Member Node. The value can be one of:

`operational`: The Member Node is operational and contributing content

`replicator`: The Member Node is operational but acts only as a replication target

`upcoming`: The Member Node is anticipated to be operational "soon".

`developing`: The Member Node is under active development and testing, should not be shown on dashboard or UI

`deprecated`: The Member Node has been deprecated and is no longer actively participating in the DataONE environment


Example: 

```xml
<property key="CN_operational_status">operational</property>
```


### `CN_date_operational`

The date that the Member Node became an operational participant in the DataONE environment. This should be the same time as when `CN_operational_status` is set to `operational` or `replicator`.

Example:

```xml
<property key="CN_date_operational">2017-03-20T15:25:53.514Z</property>
```


### `CN_date_upcoming`

The date that the Member Node became designated as `upcoming`, meaning it is expected to soon be participating in an operational capacity. This should be the same time as when `CN_operational_status` is set to `upcoming`.

Example:

```xml
<property key="CN_date_upcoming">2017-03-20T15:25:53.514Z</property>
```


### `CN_date_deprecated`

The date that the Member Node became deprecated from further particpation in the DataONE environment. This should be the same time as when `CN_operational_status` is set to `deprecated`.

Example:

```xml
<property key="CN_date_deprecated">2017-03-20T15:25:53.514Z</property>
```


### `CN_logo_url`

The URL of the logo that is to be shown for the Member Node in user ingterfaces. Note that the protocol SHOULD be `https`.

Example:

```xml
<property key="CN_logo_url">https://raw.githubusercontent.com/DataONEorg/member-node-info/master/production/graphics/web/KNB.png</property>
```


### `CN_info_url`

A URL that provides additional information about the Member Node and its host. This may for example, point to a landing page describing the data repository being represented by the Member Node.

Example:

```xml
<property key="CN_logo_url">https://knb.ecoinformatics.org/</property>
```


## Getting and Setting Custom Properties

Custom Member Node properties are typically set directly in the Coordinating Node LDAP service where node information is stored.

A python script, [`d1nodeprops`](https://github.com/DataONEorg/DataONE_Operations/blob/master/scripts/d1nodeprops) is available to get and set custom node properties. It is necessary for the CN administrator to create an `ssh` tunnel to a Coordinating Node forwarding the LDAP connection for the script to work. For example, to set the `CN_logo_url` for the node `urn:node:KNB`:

```bash
ssh -L 3890:localhost:389 cn-ucsb-1.dataone.org

#in another terminal
d1nodeprops -I "urn:node:KNB" -k "CN_logo_url" -p "SOME PASSWORD" -o update \
  "https://raw.githubusercontent.com/DataONEorg/member-node-info/master/production/graphics/web/KNB.png"
```

To list the custom properties that have been set for a Member Node:

```bash
d1nodeprops -I "urn:node:KNB" -p "SOME PASSWORD"
```
