# Language gallery

The local Highlight.js bundle contains all 193 languages included in version 11.12.0. Explicit language labels keep highlighting predictable and avoid expensive autodetection.

## Python

~~~python
from math import sqrt

def rms(samples):
    """Root mean square of a nonempty sequence."""
    return sqrt(sum(value ** 2 for value in samples) / len(samples))

print("RMS:", rms([1.0, -2.0, 3.0]))
~~~

## Lua

~~~lua
local function factorial(n)
    if n <= 1 then
        return 1
    end
    return n * factorial(n - 1)
end

print("factorial", factorial(6))
~~~

## C

~~~c
#include <stdio.h>

double average(const double *values, unsigned int count) {
    double total = 0.0;
    for (unsigned int i = 0; i < count; ++i) {
        total += values[i];
    }
    return total / count;
}
~~~

## C++

~~~cpp
#include <iostream>
#include <vector>

template <typename T>
T sum(const std::vector<T>& values) {
    T total{};
    for (const auto& value : values) total += value;
    return total;
}

int main() {
    std::cout << sum(std::vector<double>{1.0, 2.5}) << '\n';
}
~~~

## Java

~~~java
import java.util.List;

public class Measurements {
    public static double mean(List<Double> values) {
        return values.stream()
                     .mapToDouble(Double::doubleValue)
                     .average()
                     .orElseThrow(IllegalArgumentException::new);
    }
}
~~~

## Fortran: free form

~~~fortran
program mean_value
  implicit none
  real(8), dimension(3) :: values = [1.0d0, 2.0d0, 3.0d0]
  real(8) :: result
  result = sum(values) / size(values)
  print *, "Mean:", result
end program mean_value
~~~

## Fortran: fixed form

~~~fortran
C     FIXED-FORM EXAMPLE
      PROGRAM SUMSQ
      INTEGER I
      REAL TOTAL
      TOTAL = 0.0
      DO 10 I = 1, 10
         TOTAL = TOTAL + I * I
   10 CONTINUE
      PRINT *, TOTAL
      END
~~~

## Bash

~~~bash
#!/usr/bin/env bash
set -euo pipefail
for source in docs/*.md; do
    printf 'Checking %s\n' "$source"
done
python -m mkdocs build --strict
~~~

## PowerShell

~~~powershell
$pages = Get-ChildItem -LiteralPath .\docs -Filter *.md -Recurse
foreach ($page in $pages) {
    Write-Host "Checking $($page.Name)"
}
python -m mkdocs build --strict
~~~

## YAML

~~~yaml
site_name: Internal documentation
use_directory_urls: false
theme:
  name: readthedocs
  custom_dir: theme
plugins:
  - best-offline
~~~

## JSON

~~~json
{
  "network_required": false,
  "platforms": ["rhel7", "rhel9", "windows"],
  "features": {"search": true, "math": true}
}
~~~

## SQL

~~~sql
SELECT instrument, AVG(value) AS mean_value
FROM measurements
WHERE recorded_at >= '2026-01-01'
GROUP BY instrument
ORDER BY instrument;
~~~

## Plain output

~~~text
Documentation built successfully.
Open site/index.html to begin reading.
~~~
