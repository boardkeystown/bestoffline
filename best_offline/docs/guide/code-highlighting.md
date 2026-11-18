# Code highlighting

For clickable function names inside highlighted code, see [clickable cheat sheets](cheat-sheets.md). Ordinary code fences intentionally display links as literal code.

Give a fenced code block a language label to enable the theme's local Highlight.js coloring. The examples below show exactly what to write in Markdown and how it appears.

## Fence syntax

Start a block with three backticks followed by the language. Put three backticks on their own line to close it.

**Write this:**

~~~~markdown
```python
print("Hello from our documentation")
```
~~~~

**Result:**

~~~python
print("Hello from our documentation")
~~~

Three tildes, as in <code>~~~python</code>, also work. Use the same kind of fence to open and close a block, and leave a blank line before and after it.

The language label is <code>python</code>, not a filename such as <code>example.py</code>.

## Python

This example calculates an arithmetic mean and works with Python 3.6.

**Markdown source:**

~~~~markdown
```python
def mean(values):
    """Return the arithmetic mean of a nonempty sequence."""
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)

samples = [2.0, 4.0, 6.0]
print("Mean: {:.1f}".format(mean(samples)))
```
~~~~

**Rendered code:**

~~~python
def mean(values):
    """Return the arithmetic mean of a nonempty sequence."""
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)

samples = [2.0, 4.0, 6.0]
print("Mean: {:.1f}".format(mean(samples)))
~~~

Save the code inside the fences as <code>mean.py</code> to run it:

~~~bash
python mean.py
~~~

**Expected output:**

~~~text
Mean: 4.0
~~~

## Lua

Use the <code>lua</code> language label. This example uses the same sample values as the Python version.

**Markdown source:**

~~~~markdown
```lua
local function mean(values)
    if #values == 0 then
        error("values must not be empty")
    end

    local total = 0
    for _, value in ipairs(values) do
        total = total + value
    end
    return total / #values
end

local samples = {2.0, 4.0, 6.0}
print(string.format("Mean: %.1f", mean(samples)))
```
~~~~

**Rendered code:**

~~~lua
local function mean(values)
    if #values == 0 then
        error("values must not be empty")
    end

    local total = 0
    for _, value in ipairs(values) do
        total = total + value
    end
    return total / #values
end

local samples = {2.0, 4.0, 6.0}
print(string.format("Mean: %.1f", mean(samples)))
~~~

If Lua is installed, save the code as <code>mean.lua</code> and run:

~~~bash
lua mean.lua
~~~

**Expected output:**

~~~text
Mean: 4.0
~~~

## C++

Use <code>cpp</code> as the language label. This example uses C++11 features.

**Markdown source:**

~~~~markdown
```cpp
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

double mean(const std::vector<double>& values) {
    if (values.empty()) {
        throw std::invalid_argument("values must not be empty");
    }
    double total = 0.0;
    for (double value : values) {
        total += value;
    }
    return total / values.size();
}

int main() {
    const std::vector<double> samples{2.0, 4.0, 6.0};
    std::cout << "Mean: " << std::fixed << std::setprecision(1)
              << mean(samples) << '\n';
}
```
~~~~

**Rendered code:**

~~~cpp
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

double mean(const std::vector<double>& values) {
    if (values.empty()) {
        throw std::invalid_argument("values must not be empty");
    }
    double total = 0.0;
    for (double value : values) {
        total += value;
    }
    return total / values.size();
}

int main() {
    const std::vector<double> samples{2.0, 4.0, 6.0};
    std::cout << "Mean: " << std::fixed << std::setprecision(1)
              << mean(samples) << '\n';
}
~~~

If a C++ compiler is installed, save the code as <code>mean.cpp</code>. With GCC on Linux:

~~~bash
g++ -std=c++11 mean.cpp -o mean
./mean
~~~

**Expected output:**

~~~text
Mean: 4.0
~~~

MkDocs displays these programs; it does not execute or compile them. Lua and a C++ compiler are optional tools for running the examples and are not needed to build or read the documentation.

## Language labels

| Code | Recommended label |
| --- | --- |
| Python | <code>python</code> |
| Lua | <code>lua</code> |
| C | <code>c</code> |
| C++ | <code>cpp</code> |
| Java | <code>java</code> |
| Fortran | <code>fortran</code> |
| Bash | <code>bash</code> |
| PowerShell | <code>powershell</code> |
| YAML / JSON | <code>yaml</code> / <code>json</code> |
| LaTeX source | <code>latex</code> |
| Logs or unformatted output | <code>text</code> |

See the [language gallery](../reference/languages.md) for more rendered examples.

## Inline code and plain output

Use single backticks for an identifier in a sentence:

~~~markdown
Call `mean(values)` after checking the input.
~~~

**Result:** Call <code>mean(values)</code> after checking the input.

Inline code is styled as code, but this theme applies language highlighting only to fenced blocks. For logs and output, use a <code>text</code> fence:

~~~~markdown
```text
Processed 3 samples.
Mean: 4.0
```
~~~~

## Copying and appearance

The theme adds a language label and a Copy button above each fenced block. Copy grabs only the code inside the block, not the Markdown fences.

Switch between light and dark mode to change the code palette. All language definitions and styles are bundled locally.

## If highlighting does not appear

- Check the language spelling and make sure the closing fence is present.
- Keep fences at the top level of the Markdown page. The current standard <code>fenced_code</code> extension does not support nesting fences inside lists or blockquotes.
- Rebuild after changing the source, then refresh the generated page.
- Allow local JavaScript, or use the optional localhost server if browser policy restricts it.

Unlabelled blocks and unknown languages remain plain text in this theme; it does not guess a language.

To display an equation rather than its source code, use the delimiters in the [LaTeX mathematics guide](../reference/math.md).

Optional online reference: [Python-Markdown fenced code blocks](https://python-markdown.github.io/extensions/fenced_code_blocks/).
