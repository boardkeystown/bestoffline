# LaTeX mathematics

Write equations directly in Markdown using LaTeX math syntax. This project already includes the Markdown math extension and a local MathJax renderer, so no additional installation or internet connection is needed.

Each example below includes the source to copy and its rendered result.

## Inline notation

Put a single dollar sign on each side of an expression to place it within a sentence. Keep the expression next to the delimiters, without padding spaces.

**Write this:**

~~~markdown
The energy relation is $E = mc^2$.
For $n$ measurements, the mean is $\bar{x}$.
~~~

**Result:** The energy relation is $E = mc^2$. For $n$ measurements, the mean is $\bar{x}$.

## Display equations

For a centered equation on its own line, put double dollar signs on separate lines around it. Leave a blank line before and after the block.

**Write this:**

~~~latex
$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$
~~~

**Result:**

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

Do not put the dollar-delimited block inside a code fence when you want it rendered. A code fence deliberately displays the source, as in the examples on this page.

## Common notation

Use braces to group a subscript, exponent, numerator, or denominator containing more than one character.

| Meaning | Source inside math delimiters | Result |
| --- | --- | --- |
| Subscript and exponent | <code>x_i^2</code> | $x_i^2$ |
| Grouped subscript | <code>x_{i+1}</code> | $x_{i+1}$ |
| Grouped exponent | <code>e^{-\lambda t}</code> | $e^{-\lambda t}$ |
| Fraction | <code>\frac{a+b}{c}</code> | $\frac{a+b}{c}$ |
| Square root | <code>\sqrt{x^2+y^2}</code> | $\sqrt{x^2+y^2}$ |
| Greek symbols | <code>\alpha, \beta, \theta, \Delta</code> | $\alpha, \beta, \theta, \Delta$ |
| Vector | <code>\mathbf{x}</code> | $\mathbf{x}$ |
| Comparison | <code>a \leq b \neq c</code> | $a \leq b \neq c$ |
| Real numbers | <code>x \in \mathbb{R}</code> | $x \in \mathbb{R}$ |
| Text and units | <code>v = 3\,\text{m/s}</code> | $v = 3\,\text{m/s}$ |

Commands such as <code>\sin</code> and <code>\log</code> format function names upright. Use <code>\text{...}</code> for ordinary words inside mathematics.

## Sums, integrals, and derivatives

**Write this:**

~~~latex
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$
~~~

**Result:**

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

$$
\frac{\partial u}{\partial t} = \alpha \nabla^2 u
$$

The commands <code>_</code> and <code>^</code> supply lower and upper limits. The command <code>\,</code> inserts a small amount of spacing.

## Matrices

Use <code>&amp;</code> between columns and <code>\\</code> between rows. The <code>bmatrix</code> environment supplies square brackets; <code>pmatrix</code> supplies parentheses.

**Write this:**

~~~latex
$$
A =
\begin{bmatrix}
1 & 2 & 3 \\
0 & 1 & 4 \\
5 & 6 & 0
\end{bmatrix},
\qquad
A\mathbf{x} = \mathbf{b}
$$
~~~

**Result:**

$$
A =
\begin{bmatrix}
1 & 2 & 3 \\
0 & 1 & 4 \\
5 & 6 & 0
\end{bmatrix},
\qquad
A\mathbf{x} = \mathbf{b}
$$

The command <code>\qquad</code> adds horizontal spacing between the matrix and the following expression.

## Aligned derivation

Use <code>aligned</code> for several related lines. Put <code>&amp;</code> at the alignment position and <code>\\</code> at each line break.

**Write this:**

~~~latex
$$
\begin{aligned}
\operatorname{Var}(X)
  &= \mathbb{E}\left[(X-\mu)^2\right] \\
  &= \mathbb{E}[X^2] - 2\mu\mathbb{E}[X] + \mu^2 \\
  &= \mathbb{E}[X^2] - \mu^2
\end{aligned}
$$
~~~

**Result:**

$$
\begin{aligned}
\operatorname{Var}(X)
  &= \mathbb{E}\left[(X-\mu)^2\right] \\
  &= \mathbb{E}[X^2] - 2\mu\mathbb{E}[X] + \mu^2 \\
  &= \mathbb{E}[X^2] - \mu^2
\end{aligned}
$$

Here <code>\mu = \mathbb{E}[X]</code>. The <code>\left</code> and <code>\right</code> commands size the surrounding brackets.

## Numbering and references

This theme enables AMS equation numbering. Wrap a numbered expression in <code>equation</code>, assign a unique <code>\label{...}</code>, and refer to it with <code>\eqref{...}</code>.

**Write this:**

~~~latex
$$
\begin{equation}
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
\label{eq:gauss}
\end{equation}
$$

Equation $\eqref{eq:gauss}$ expresses Gauss's law.
~~~

**Result:**

$$
\begin{equation}
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
\label{eq:gauss}
\end{equation}
$$

Equation $\eqref{eq:gauss}$ expresses Gauss's law.

Labels and equation references work within the current page. For another page, use a [Markdown heading link](../guide/links.md#link-to-a-heading) to its equation section. Ordinary display blocks are unnumbered; <code>equation*</code> also suppresses numbering.

## Cases and symbols

Use <code>cases</code> for a piecewise definition. Put the expression before <code>&amp;</code> and its condition after it.

**Write this:**

~~~latex
$$
f(x) =
\begin{cases}
x^2, & x \geq 0,\\
-x, & x < 0.
\end{cases}
\qquad
\forall x \in \mathbb{R}
$$
~~~

**Result:**

$$
f(x) =
\begin{cases}
x^2, & x \geq 0,\\
-x, & x < 0.
\end{cases}
\qquad
\forall x \in \mathbb{R}
$$

## Literal dollar signs

Escape a dollar sign used as ordinary text with a backslash:

~~~markdown
The example cost is \$5.
~~~

**Result:** The example cost is \$5.

For a literal formula that should not be typeset, put it in inline code or a fenced <code>latex</code> block. This is useful when documenting the syntax itself.

## If an equation does not render

| Symptom | Check |
| --- | --- |
| Source appears as a code block | Remove the surrounding code fence if you want rendered mathematics. |
| Dollar signs remain visible | Match the opening/closing delimiters; keep inline expressions next to their dollar signs. |
| A matrix or derivation fails | Match each begin/end environment and check braces, column separators, and row breaks. |
| A reference is unresolved | Check the label spelling, keep labels unique, and keep the reference on the same page. |
| No equations render | Rebuild and allow local JavaScript; use localhost if browser policy blocks local scripts. |

The supported syntax is MathJax's TeX mathematics subset. Full LaTeX documents, document classes, and arbitrary packages are not part of this renderer.

The local SVG renderer handles the displayed equations without fetching browser fonts. Switch the theme between light and dark mode to inspect the same formulas in both appearances.

Optional online references: [Arithmatex input syntax](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/) and [MathJax equation numbering](https://docs.mathjax.org/en/v3.2/input/tex/eqnumbers.html).
