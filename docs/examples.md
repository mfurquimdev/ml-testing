# Material Mkdocs Examples


## Keyboard keys

Press ++ctrl+c++ to exit.


## Critic example

Here is some {--*incorrect*--} Markdown. I am adding this{++ here++}.  
And here is a comment on {==some text==}{>>This works quite well. I just wanted to comment on it.<<}.

Substitutions {~~is~>are~~} great!

## Code blocks


### Diff

``` diff

- a = 1
+ a = 2
```


``` py linenums="1" hl_lines="2 3" title="bubble_sort.py"
# TODO: Here I am, a comment
CONSTANT_VALUE = "Hello World"
def bubble_sort(items):
    i := 0
    lambda j: j < len(items)
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return "Hello World" # (1)!
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

### Mermaid

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```


## Sortable Table

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | :material-check:     Fetch resource  |
| `PUT`       | :material-check-all: Update resource |
| `DELETE`    | :material-close:     Delete resource |


## Notes

!!! note
    This is a note.

!!! note ""
    This is a note without a title.

??? note "Collapsible Note"
    This is a collapsible note

!!! abstract
    This is an abstract.

!!! info
    This is an info.

!!! tip
    This is a tip.

!!! success
    This is a success.

!!! question
    This is a question.

!!! warning
    This is a warning.

!!! failure
    This is a failure.

!!! danger
    This is a danger.

!!! bug
    This is a bug.

!!! example
    This is an example.

!!! quote
    This is a quote.

## LaTeX formulas

$p(x|y) = \frac{p(y|x)p(x)}{p(y)}$

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

\[3 < 4\]

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}
