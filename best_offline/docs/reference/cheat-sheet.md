---
wide: true
---

# Lab API cheat sheet

<p class="intro">Scan the declarations. Click a function name for its contract and an example.</p>

This is an **illustrative API**, not an installed library. Replace it with your team's functions. See [how to write this layout](../guide/cheat-sheets.md) and the [style reference](../guide/styled-content.md).

## Overview { #overview }

<div class="cheatsheet-grid">
<section class="api-group">
<h2 id="device-api">01 / Device</h2>
<pre class="linked-code"><code class="language-c">// Connect and release resources
bool <a href="#open-device">OpenDevice</a>(const char *name);
void <a href="#close-device">CloseDevice</a>(void);</code></pre>
</section>
<section class="api-group api-green">
<h2 id="sampling-api">02 / Sampling</h2>
<pre class="linked-code"><code class="language-c">// Capture measurements
int <a href="#read-samples">ReadSamples</a>(float *values, int capacity);
void <a href="#set-rate">SetRate</a>(int samplesPerSecond);</code></pre>
</section>
<section class="api-group api-purple">
<h2 id="statistics-api">03 / Statistics</h2>
<pre class="linked-code"><code class="language-c">// Reduce a sample buffer
float <a href="#mean">Mean</a>(const float *values, int count);
float <a href="#peak">Peak</a>(const float *values, int count);</code></pre>
</section>
<section class="api-group api-orange">
<h2 id="plotting-api">04 / Plotting</h2>
<pre class="linked-code"><code class="language-c">// Present the result
void <a href="#plot-line">PlotLine</a>(const float *values, int count);
void <a href="#set-title">SetTitle</a>(const char *title);</code></pre>
</section>
<section class="api-group api-green">
<h2 id="reports-api">05 / Reports</h2>
<pre class="linked-code"><code class="language-c">// Save an offline report
bool <a href="#save-csv">SaveCSV</a>(const char *path);
bool <a href="#save-plot">SavePlot</a>(const char *path);</code></pre>
</section>
<section class="api-group api-purple">
<h2 id="diagnostics-api">06 / Diagnostics</h2>
<pre class="linked-code"><code class="language-c">// Inspect status and errors
bool <a href="#is-ready">IsReady</a>(void);
const char *<a href="#last-error">LastError</a>(void);</code></pre>
</section>
</div>

## OpenDevice { #open-device }

Open a named device. Returns `true` on success. A failed call leaves the device closed; use `LastError()` for an explanation.

~~~c
if (!OpenDevice("sensor-01")) {
    fprintf(stderr, "%s\n", LastError());
    return 1;
}
~~~

## CloseDevice { #close-device }

Release the current device. Repeated calls are harmless in this example contract. Read or configure the device only after another successful `OpenDevice()`.

~~~c
CloseDevice();
~~~

[Back to overview](#overview)

## ReadSamples { #read-samples }

Fill at most `capacity` values in the caller's buffer. Return the number written, or `-1` on failure. A return of zero means no samples are currently available.

| Parameter | Contract |
| --- | --- |
| `values` | Writable buffer owned by the caller |
| `capacity` | Number of float elements available, greater than zero |
| Return value | Number written, or `-1`; inspect `LastError()` on failure |

~~~c
float values[256];
int count = ReadSamples(values, 256);
if (count > 0) {
    PlotLine(values, count);
}
~~~

## SetRate { #set-rate }

Choose a positive number of samples per second before starting acquisition. Document actual device limits here when adapting this example.

~~~c
SetRate(1000);
~~~

[Back to overview](#overview)

## Mean { #mean }

Calculate the arithmetic mean. The input must contain at least one sample.

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

~~~c
float values[] = {2.0f, 4.0f, 6.0f};
float average = Mean(values, 3);  // 4.0
~~~

## Peak { #peak }

Return the greatest absolute sample value. The input must contain at least one sample.

~~~c
float values[] = {-5.0f, 2.0f, 3.0f};
float peak = Peak(values, 3);  // 5.0
~~~

[Back to overview](#overview)

## PlotLine { #plot-line }

Draw consecutive samples as a line. The plotting function reads the buffer during the call and does not take ownership. Supply a positive count.

~~~c
float values[] = {1.0f, 3.0f, 2.0f};
PlotLine(values, 3);
~~~

## SetTitle { #set-title }

Set a plot title. This example API copies the supplied string, so the caller may release its buffer afterward.

~~~c
SetTitle("Sensor voltage");
~~~

[Back to overview](#overview)

## SaveCSV { #save-csv }

Save the most recent captured samples as comma-separated values. Returns `false` if the destination cannot be written. Relative paths are resolved against the application working directory.

~~~c
if (!SaveCSV("samples.csv")) {
    fprintf(stderr, "%s\n", LastError());
}
~~~

## SavePlot { #save-plot }

Save the current plot as a PNG image. Returns `false` if saving fails.

~~~c
if (!SavePlot("samples.png")) {
    fprintf(stderr, "%s\n", LastError());
}
~~~

[Back to overview](#overview)

## IsReady { #is-ready }

Return whether the current device can accept another read. This does not guarantee that a future read succeeds; still check the result.

~~~c
if (IsReady()) {
    int count = ReadSamples(values, 256);
    if (count > 0) PlotLine(values, count);
}
~~~

## LastError { #last-error }

Return a borrowed string describing the last failure. Copy it if you need to retain it across another API call. Never free this pointer.

~~~c
fprintf(stderr, "Capture failed: %s\n", LastError());
~~~

[Back to overview](#overview)
