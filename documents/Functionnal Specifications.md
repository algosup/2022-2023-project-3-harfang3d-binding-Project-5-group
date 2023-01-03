# harfang3d-binding

## Functionnal Specifications 

<details>
<summary>Table of contents</summary>

- [harfang3d-binding](#harfang3d-binding)
  - [Functionnal Specifications](#functionnal-specifications)
  - [Overview](#overview)
    - [What is HARFANG 3D?](#what-is-harfang-3d)
    - [What is FabGen?](#what-is-fabgen)
    - [Why rust?](#why-rust)
  - [Personas](#personas)
    - [Persona 1](#persona-1)
    - [Persona 2](#persona-2)
    - [Persona 3](#persona-3)
  - [Laws and regulations](#laws-and-regulations)
  - [Functionalities](#functionalities)
    - [Compatibility](#compatibility)
    - [Documentation](#documentation)
  - [Non functional requirements](#non-functional-requirements)
    - [Performance](#performance)
    - [Security](#security)
    - [Usability](#usability)
    - [Maintainability](#maintainability)
  - [Risks and assumptions](#risks-and-assumptions)
  - [Glossary](#glossary)
</details>

## Overview 

The goal of the project is to create a binding in rust for the HARFANG 3D and their 3D engine, they have a binding generator called FabGen that already supports the binding for C++/python/Lua and Go.

The point of this project is to give an access to the HARFANG 3D engine in more languages and in this case in rust, this will allow more people to use the engine and to use it for their projects.

The project is due to be done the 17th february 2023.

### What is HARFANG 3D?

HARFANG 3D is a 3D engine written in C++ that is cross platform and open source. It is mainly used to develop industrial applications like simulation, data visualization, and Augmented Reality.

The approach of the engine is based on the openness and flexibility. It was created to fit the requirements of the industrial applications which consist in:
- No dynamic memory allocation (everything is pre-allocated)

### What is FabGen?

Fabgen is a set of Python scripts to generate C++ binding code to different languages. It was written as a SWIG replacement 
It is used by HARFANG 3D to generate the binding for python, Lua and Go.

### Why rust?

Rust is a programming language that is designed to be fast, reliable and productive. It is a new language that is used to create low level application exactly like C++ but with a lot of new features that make it easier to work with and to maintain.

FabGen already supports the binding for C++/python/Lua and Go, but it does not support rust yet.

With all of these features and the rise of rust, it is a good idea to add the support for rust for FabGen.

## Personas

### Persona 1
```
Name: Lonus Tirvalds
Age: 45
Job: Data scientist 

Description:
Lonus is a data scientist, he uses HARFANG 3D to visualize the data in 3dimensions collected from a VR simulation to determine the human behavior in a specific situation.
```

### Persona 2
```
Name: Harry webb
Age: 30
Job: Software engineer for the government

Description:
Harry is a software engineer, he uses HARFANG 3D to create high quality simulations for the government with a software that respects the laws and regulations required for his job. 
```

### Persona 3
```
Name: Lena Nelson
Age: 25
Job: Engineer for a car company

Description:
Lena is an engineer for a car company, she uses HARFANG 3D to create AR tools for the head-up display of a car. 
```

## Laws and regulations

For this kind of software, there are a lot of laws and regulations that must be respected. The most important ones are:
- no dynamic memory allocation
- ISO 26262 
- MISRA 
- AutoSAR

## Functionalities

We need to implement an access to all of the available functionalities of the HARFANG 3D engine in rust.

### Compatibility

The binding needs to be compatible with the versions of the engine that are available on the github repository,

### Documentation

The binding needs to be documented in the same way as the engine,

## Non functional requirements

### Performance

The binding must be as fast as possible, the engine is already very fast and we need to keep it that way.

### Security

The binding must stay in the same security expectations as the engine.

### Usability

The binding must be easy to use and to understand for the user.

### Maintainability

The binding must be easy to maintain and to update for the developer.

## Risks and assumptions

The main risks are:
- The binding is not compatible with all the features of the engine
- The binding is not as fast as other bindings in other languages
- The binding is not as easy to use as other bindings in other languages
- The binding is not as easy to maintain as other bindings in other languages
- The binding does not respect the laws and regulations required to be used in some industries
- The binding is not well documented and is confusing for the user 
- The binding is difficult to be maintained and updated
- The binding is not compatible with the latest version of the engine and is difficult to update 

With all of these concerns, the binding might be deprecated and not used anymore.

To prevent this from happening, the binding needs to be think and designed in a way that it is easy to maintain and update through the time. 

We need to make sure that the binding will be usefull and adapted to the future needs of the engine.

## Glossary

- Binding: a binding is a way to access a library in a different language than the one it was written in. 

- Rust: Rust is a programming language that is designed to be fast, reliable and productive. It is a compiled language that is used to create low level software like operating systems, device drivers, and embedded software. 

- 3D engine : A 3D engine is a software that is used to create 3D applications. It is used to create 3D games, simulations, and data visualization.

- SWIG: SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages.

- Data scientist: A data scientist is a person who is skilled in extracting knowledge or insights from data in various forms, either structured or unstructured, similar to a data analyst but more focused on advanced analysis and modeling techniques.

- AR : Augmented reality is a live direct or indirect view of a physical, real-world environment whose elements are augmented by computer-generated sensory input such as sound, video, graphics or GPS data.

- VR: Virtual reality is a computer technology that uses virtual reality headsets, sometimes in combination with physical spaces or multi-projected environments, to generate realistic images, sounds and other sensations that simulate a user's physical presence in a virtual or imaginary environment.

- ISO 26262: ISO 26262 is an international standard for road vehicles that specifies the functional safety requirements for electrical and/or electronic systems and their software. It is a part of the ISO 26200 series of standards for road vehicles. 

- MISRA: MISRA is an independent, organization that provides coding standards for the development of embedded software, that specifies a set of rules for the C and C++ programming languages in order to keep the code consistent and to avoid common programming mistakes.

- AutoSAR: AutoSAR is a set of guidelines for the development of software for automotive electronic control units (ECUs). It is based on the AUTOSAR standard and is used in the automotive industry, however it is not necessary to use it to develop the infotainment system of a car.