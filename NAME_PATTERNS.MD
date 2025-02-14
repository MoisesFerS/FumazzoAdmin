# NAME PATTERNS  

This document describes the naming patterns used throughout the project to maintain consistency and ease of maintenance. These conventions are designed to improve readability, scalability, and facilitate collaboration among team members.  

---

## PADRONIZING  

This process aims to eliminate inconsistencies in the naming of elements, IDs, and classes, as well as variables and functions used within the project. By following the formula listed below for each topic, the code becomes more organized and maintainable.  

---

## HTML ELEMENTS

Pattern for the elements created from HTML.

## NAME AND ID

To name or give id to an element, use simple names that can describe its function or values that represent its purpose.

The names **_MUST_** be:
- Lowercase.
- Maximum of three components.

## CLASS

The element class should be composed of:

[context/local]-[context/local]*-[element/purpose]-[variant/state]-[action/behavior]*-[theme/style]*
*only if needed

The classes **_MUST_** be:
- Lowercase.
- Single words.

Do not use:
- Composed names to one segment. Ex: loginForm or login-form.

#### Context/Local - Obligatory

Describes the element context or where the element is located. The context have a priority over the location Examples:

#### Context - In which context is the element being used

- modal
- accordion

#### Local - Where is the element located

- navbar
- footer
- main
- table

Global generic elements(Ex: buttons, inputs, etc.) doesn't need this segment. 

#### Element/Purpose - Obligatory

The element tag or its use. Examples:

- button
- input
- form

For some tags, use its purpose instead of the tag. Examples:

- h1 = title
- h2 = subtitle
- p = text/description/data
- hr = separation/division
- div/section = container/content

#### Variant/State - Obligatory, if the element has one

Describes the element variant or its present state. Examples:

#### Variant - The pre-set of an element

- primary
- secondary

#### State - Which state is the element at this moment

- active
- inactive
- visible
- invisible

#### Action/Behavior - Optional

Describes the element action or behavior at the context. Examples:

- open
- closed
- expanded
- retract

#### Theme/Style - Optional

Describe the element theme or style. Examples:

- dark
- light

#### EXAMPLES

navbar-dropdown-button-primary-dark
A button located at a navbar dropdown, using the primary pre-set with a dark style.

accordion-row-division
Just a line making a division at an accordion row.

modal-header-title
A title at a modal's header.

---