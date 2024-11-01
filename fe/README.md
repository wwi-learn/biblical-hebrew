# Opus UI Example Application

This project serves as an example of how to build an Opus UI application. 

## Getting started
1. Clone this repository
2. `npm i`
3. `npm start`

## Pure vs Hybrid
By default, this example application renders a [pure Opus UI application](#pure-applications).

If you want to render a [hybrid Opus UI application](#hybrid-applications) instead, rename the `main.jsx` file to `mainPure.jsx` and rename `mainHybrid.jsx` to `main.jsx`

## Pure Applications
Pure applications are characterized by consisting 'mostly' of JSON files. This still allows for custom component types and script actions to be defined and used within your JSON files. 

This is the recommended way to build new applications using Opus UI.

## Hybrid Applications
When you want to add Opus UI to an existing application you will likely want to build a hybrid application. These types of applications have lots of custom components that aren't necessarily registered as Opus UI component types. Additionally, they will also have various extra features already built in (like global state management and routing).
