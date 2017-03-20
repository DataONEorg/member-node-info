# Custom Member Node Properties

Member Nodes generally control the content available in the Member Node document provided through the [/node](https://cn.dataone.org/cn/v2/node) service. This document describes custom properties that may be set by the Coordinating Nodes to augment the information provided by the Member Nodes. Such custom properties are not over-written by a Member Node when the Member Node registration information is updated.

Custom properties set by the Coordinating Nodes MUST be prefixed by `CN_`. Such properties will be preserved through updates to the node registration.

## Preferred Custom Properties

The following custom properties are used by systems such as the DataONE [search interface](https://search.dataone.org) and [Member Node dashboard](https://www.dataone.org/current-member-nodes).

### `CN_node_name`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_node_name']
```

Provides the same information as the [`name`](https://releases.dataone.org/online/api-documentation-v2.0/apis/Types.html#Types.Node.name) element of the node document though may optionally be augmented by DataONE to provide additional or clarifying details.

Example XML node document snippet 
```
  <property key="CN_node_name">node name text string</property>
```

### `CN_operational_status`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_operational_status']
```
Indicates the current operational status of the Member Node. The value can be one of:

`operational`: The Member Node is operational and contributing content
`replication`: The Member Node is operational but acts only as a replication target
`upcoming`: The Member Node is anticipated to be operational "soon".
`developing`: The Member Node is under active development and testing, should not be shown on dashboard or UI
`deprecated`: The Member Node has been deprecated and is no longer actively participating in the DataONE environment

### `CN_date_operational`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_date_operational']
```

### `CN_date_upcoming`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_date_upcoming']
```

### `CN_date_deprecated`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_date_deprecated']
```


### `CN_logo_url`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_logo_url']
```


### `CN_info_url`

XPath location, ${NODE_ID} is replaced by the node identifier, e.g. "urn:node:mnDemo6": 
 
```
  //node[identifier/text()='${NODE_ID}']/property[@key='CN_info_url']
```


## Miscellaneous

Use XML Starlet to select and show individual node document from CN `/node` response:

```
curl -q "https://cn-dev.test.dataone.org/cn/v2/node" | xml sel -t -m "//node[identifier/text() = 'urn:node:mnDemo6']" -c .

```

