# Clickable cheat sheets

Yes: a code-looking reference can contain real links to detailed explanations. Open the [example API cheat sheet](../reference/cheat-sheet.md) to try a wide grid of grouped declarations. Click a function name to jump down to its documentation.

The layout takes inspiration from the [raylib cheat sheet](https://www.raylib.com/cheatsheet/cheatsheet.html): compact declarations grouped by module. Our example uses an invented lab API so you can replace the names and descriptions with your own. The example and all its assets are included locally.

## Why a normal code fence cannot contain links

Fenced code deliberately displays its contents literally. This shows Markdown source; it does not create a clickable link:

~~~~markdown
~~~c
int [ReadSamples](#read-samples)(float *values, int capacity);
~~~
~~~~

Use a raw HTML `pre` block with the opt-in `linked-code` class when you want real links. The theme highlights the complete code, preserves the anchors, and copies only the plain code text.

## A linked code block

**Write this directly in your Markdown file, outside a code fence:**

~~~html
<pre class="linked-code"><code class="language-c">int <a href="#read-samples">ReadSamples</a>(float *values, int capacity);
void <a href="#close-device">CloseDevice</a>(void);</code></pre>
~~~

**Result:**

<pre class="linked-code"><code class="language-c">int <a href="#read-samples">ReadSamples</a>(float *values, int capacity);
void <a href="#close-device">CloseDevice</a>(void);</code></pre>

Then create matching sections with explicit IDs:

~~~markdown
## ReadSamples { #read-samples }

Explain the parameters, return value, and an example.

## CloseDevice { #close-device }

Explain when to release the device.
~~~

### ReadSamples { #read-samples }

This illustrative function fills a caller-provided buffer and returns the number of samples written, or a negative error code. In your own documentation, specify units, valid sizes, errors, and ownership.

### CloseDevice { #close-device }

This illustrative function releases the device. State whether repeated calls are safe and what other functions may be called afterward.

## Linking a whole signature

You can link just a function name, a type, a comment, or the whole signature. The syntax colors stay intact even when the link spans multiple tokens:

~~~html
<pre class="linked-code"><code class="language-cpp"><a href="#sample-buffer">std::vector&lt;float&gt; ReadSamples(int count);</a>
bool <a href="#sample-buffer" title="Buffer ownership and limits">Ready</a>(const Buffer&amp; buffer);</code></pre>
~~~

**Result:**

<pre class="linked-code"><code class="language-cpp"><a href="#sample-buffer">std::vector&lt;float&gt; ReadSamples(int count);</a>
bool <a href="#sample-buffer" title="Buffer ownership and limits">Ready</a>(const Buffer&amp; buffer);</code></pre>

### Sample buffer { #sample-buffer }

This target demonstrates whole-signature links and escaped C++ characters. Clicking either declaration reaches this paragraph. The Copy button produces `std::vector<float>` and `Buffer&`, without HTML tags or entities.

For raw HTML, encode code characters `<` as `&lt;`, `>` as `&gt;`, and `&` as `&amp;`. The `<a>` tags themselves must remain HTML. Keep actual line breaks between declarations; `pre` preserves them.

## Build the reference grid

Start a new page with this metadata to use the available width:

~~~yaml
---
wide: true
---
~~~

Then add a title and groups. Each group needs a unique heading ID; each declaration should link to a unique detail heading below the grid.

~~~html
<div class="cheatsheet-grid">
  <section class="api-group">
    <h2 id="device-api">Device</h2>
    <pre class="linked-code"><code class="language-c">int <a href="#read-samples">ReadSamples</a>(float *values, int capacity);
void <a href="#close-device">CloseDevice</a>(void);</code></pre>
  </section>
  <section class="api-group api-green">
    <h2 id="statistics-api">Statistics</h2>
    <pre class="linked-code"><code class="language-c">float <a href="#mean">Mean</a>(const float *values, int count);</code></pre>
  </section>
</div>
~~~

Use ordinary Markdown below the closing `</div>` for the detail headings, prose, tables, math, and fenced examples. For the snippet above, add headings with IDs `read-samples`, `close-device`, and `mean`. The [complete example source](../reference/cheat-sheet.md) shows this structure in use.

The grid adjusts its column count to the available width; phones get a single column. Long declarations scroll inside their own group. The left navigation remains available, and `wide: true` hides the right-hand table of contents. Omit that setting for a regular-width article.

Available group colors are the default blue and the optional classes `api-green`, `api-purple`, and `api-orange`. Use color to reinforce the visible module name, not as the only identifier.

## Link to another page

Inside raw HTML code, use an HTML output path:

~~~html
<a href="../reference/cheat-sheet.html#mean">Mean</a>
~~~

Outside raw HTML, use a normal Markdown source link:

~~~markdown
[Mean](../reference/cheat-sheet.md#mean)
~~~

Both work when opening the built site directly from disk. Do not begin local paths with `/`; keep them relative. Explicit IDs keep links stable when you rename a heading. Avoid duplicate IDs on a large reference page.

## Reading, copying, and accessibility

- Underlined code text is clickable. Tab and Enter also work.
- The Copy button copies the displayed code, without link markup.
- Links work even when JavaScript is disabled; syntax coloring and Copy need JavaScript.
- The linked-code behavior supports the same bundled languages as ordinary code fences.
- Write real descriptions below the overview so search can find parameters, concepts, and examples.
- Include a normal Markdown “Back to overview” link after long explanations.

See [cards and styled content](styled-content.md#reusable-class-reference) for the complete reusable class list.
