# Sales Person Management System

Sales Person Management System

## 0.1.3 - 2023-01-31

## Features and Changes in 0.1.3

### New Features hello

- Make the ***Collect Goal*** doctype as a tree
- Writing the traversing tree functionality on ***Collecting*** doctype events(```on_submit, on_cancel```)

### Bug Fixes

- Refactor code on visiting doctype
- Make event **on_cancel** that do the reverse of the **on_submit** event
- Edit events on sales invoice to update the target on both way adding and subtracting(```on_submit, on_cancel```)

### Breaking Changes

- Change the custom events directory from single file in methods to structured directory in events folder
- breaks all big block of code into smaller functions and add it to the **utils.py** file

### Miscellaneous

- Generals refactors
- Cleaning the code & formatting
- Rename general functions
- Remove unnecessary **functions** and **imports**

<hr>
## 0.1.4 - 2023-02-11

## Features and Changes in 0.1.4

### New Features

- Change doctype layout to tab view(**collects goal, visit goal**)
- split layout into smaller columns to fit viewport
- add reset button ``Reset Fields`` to reset all fields in visit goal and achievements records (#30)

### Bug Fixes

- Refactor code on visiting doctype
- fix ```on_cancel``` subtraction for collecting in type ``fixed_target``

### Miscellaneous

- 
#### License

MIT
