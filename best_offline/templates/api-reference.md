---
wide: true
---

# Example API

Replace this illustrative API with your own. Keep the overview compact and the detailed contracts below it.

| Document information | Value |
| --- | --- |
| Owner | Replace with responsible team |
| Applies to | Replace with software/hardware version |
| Status | Draft |
| Last reviewed | YYYY-MM-DD |

## Overview { #overview }

<div class="cheatsheet-grid">
<section class="api-group">
<h2 id="samples-api">Samples</h2>
<pre class="linked-code"><code class="language-c">int <a href="#read-samples">ReadSamples</a>(float *values, int capacity);</code></pre>
</section>
</div>

## ReadSamples { #read-samples }

Fill a caller-owned buffer with samples. Replace this description with the real contract.

### Parameters

| Parameter | Type | Units and valid values |
| --- | --- | --- |
| values | float pointer | Writable buffer; document sample units |
| capacity | integer | Number of elements, greater than zero |

### Return value

Number of samples written, zero when no samples are available, or a negative error code. Replace these example semantics with your implementation's behavior.

### Ownership and thread safety

State who owns each buffer, how long returned pointers remain valid, and whether simultaneous calls are permitted.

### Example

~~~c
float values[256];
int count = ReadSamples(values, 256);
if (count < 0) {
    /* Handle the documented error. */
}
~~~

### Failure cases

| Condition | Result | Recovery |
| --- | --- | --- |
| Device disconnected | Replace with actual error | Replace with actual recovery |

### Related operations

Add links to initialization, cleanup, and related functions.

[Back to overview](#overview)
