# Harfang3D-binding

## Functional Specifications 

<details>
<summary>Table of contents</summary>

- [Harfang3D-binding](#harfang3d-binding)
  - [Functional Specifications](#functional-specifications)
  - [Overview](#overview)
    - [What is Harfang 3D?](#what-is-harfang-3d)
    - [What is FABGen?](#what-is-fabgen)
    - [Why Rust?](#why-rust)
  - [Audience](#audience)
  - [Personas](#personas)
    - [Persona 1](#persona-1)
    - [Persona 2](#persona-2)
    - [Persona 3](#persona-3)
    - [Persona 4](#persona-4)
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
  - [Success criteria](#success-criteria)
  - [Out of scope](#out-of-scope)
  - [Glossary](#glossary)
</details>

## Overview 

The goal of the project is to create a binding in Rust for the Harfang 3D and their 3D engine. They have a binding generator called FABGen that already supports the binding for C++/Python/Lua and Go.

The point of this project is to give access to the Harfang 3D engine in more languages and in this case in Rust, this will allow more people to use the engine and to use it for their projects.

The project is due to be done the 17th February 2023.

### What is Harfang 3D?

Harfang 3D is a 3D engine written in C++ that is cross platform and open source. It is mainly used to develop industrial applications like simulation, data visualization, and Augmented Reality.

The approach of the engine is based on openness and flexibility. It was created to fit the requirements of the industrial applications which consist in:
- No dynamic memory allocation (everything is pre-allocated)
- No exceptions (error handling is done with return codes)
- No virtual functions (everything is done with function pointers)
- ISO 26262 
- MISRA
- AutoSAR

Industries that are using Harfang 3D are using it because they need to respect a lot of strong technical requirements, for example:
- Safety certifications 
- Embeddability and custom hardware
- Low power consumption

Harfang 3D is not a competitor of other game engines like Unity or Unreal Engine since there are a lot of differences between the uses of the engines. 

Compared to other game engines, Harfang 3D has a couple of advantages for the industries:
- Open and secure license 
- Can run on premise 100% offline
- Designed to handle large amounts of data

### What is FABGen?

FABGen is a set of Python scripts to generate C++ binding code to different languages. It was written as a SWIG replacement.

It is used by Harfang 3D to generate the binding for Python, Lua and Go.

### Why Rust?

Rust is a programming language that is designed to be fast, reliable and productive. It is a new language that is used to create low level applications exactly like C++ but with a lot of new features that make it easier to work with and to maintain.

FABGen already supports the binding for Python/Lua and Go, but it does not support Rust yet.

With all of these features and the rise of Rust, it is a good idea to add the support for Rust for FABGen.

## Audience

The audience of the solution is the developers who are using the Harfang 3D engine, it will allow them to use the engine in Rust. 

A lot of developers are using Rust for their projects, and a lot of software in C++ are translated into Rust, for memory safety purposes.

In the recent surveys from the developers, Rust is one of the most popular languages in 2022 and it is expected to be the most popular language in 2023. 

Which will result in more opportunities for the engine and the people who are using it. 

## Personas

### Persona 1
```
Name: Lonus Tirvalds
Age: 45
Job: Data scientist 
Place: Berlin, Germany

Behaviors: Lonus to do his job efficiently and use the most optimal tools for his job. He is using Harfang 3D in C++ and python

Description:
Lonus is a data scientist, he uses Harfang 3D to visualize the data in 3Dimensions collected from a VR simulation to determine human behavior in a specific situation.

Needs & goals: Lonus wants to have the fastest, the most efficient and the most secure way to visualize the data he is collecting from a VR simulation.

Use case: Lonus is interested about learning and using Rust, to be more efficient and to have a better performance in his job, it will also bring him new opportunities for his carrer to learn a new language.
```

### Persona 2
```
Name: Harry webb
Age: 30
Job: Software engineer for the government
Place: Zurich, Switzerland

Description:
Harry is a software engineer, he uses Harfang 3D to create high quality simulations for the government with a software that respects the laws and regulations required for his job. 

Needs & goals: Harry wants to use a good 3D engine that respects everything his employer asked, he is using Harfang 3D in Go however he also needs to treat the data and he is using a Rust program to create graph with them.

Use case: Harry wants to use the same language for his 3D engine and for his data treatment, which will improve his productivity, he will be able to focus on only one language and not have to switch between them.
```

### Persona 3
```
Name: Lena Nelson
Age: 25
Job: Manager for a car company
Place: London, UK

Description:
Lena is a manager for a car company, her employees use Harfang 3D to create AR tools for the head-up display of a car.

Needs & goals: Lena wants to standardize the tools her employees are using, she wants to use the same language for everything, and on top of that she wants to use a modern language for this kind of work.

Use case: Lena have chosen Rust for the new tools her employees will be using, she wants everyone to use the same language, which will make it easier for them to work together. Our solution will allow her to do that.
```

### Persona 4
```
Name: John Doe
Age: 30
Job: Kernel developer

Description: John is a kernel developer, he is creating an embedded system for a VR headset in Rust, which is supposed to be used with an Harfang 3D simulation in it, he also would like to use only one language for everything, Rust is the best choice for him. However he is currently using Harfang 3D in C++.

Needs & goals: John wants to have the most optimal performance for his system, he also wants to use an open-source 3D engine, he has strong requirements towards the engine, he wants to provide the most optimal experience for the users of his VR headset.

Use case: John wants to use Rust for everything, with our solution he will be able to use Harfang 3D in Rust, which will allow him to use only one language for everything.
``` 

## Laws and regulations

For this kind of software, there are a couple of laws and regulations that must be respected. The most important ones are:
- No dynamic memory allocation
- ISO 26262 
- MISRA 
- AutoSAR

## Functionalities

We need to implement an access to all of the available functionalities of the Harfang 3D engine in Rust.

### Compatibility

The binding needs to be compatible with the versions of the engine that are available on the GitHub repository.

The binding needs to be compatible with the latest version of the engine.

### Documentation

The binding needs to be documented in the same way as the engine. The documentation needs to be clear and easy to understand for the user. 

The documentation needs to be available on the GitHub repository of the project.

## Non functional requirements

### Performance

The binding must be as fast as possible, the engine is already very fast and we need to keep it that way.

It also needs to be as fast as other bindings in other languages.

### Security

The binding must stay in the same security expectations as the engine.

### Usability

The binding must be easy to use and to understand for the user.

The binding must be directly usable by the user without any additional work.

### Maintainability

The binding must be easy to maintain and update for the developer.

We need to provide all the documentation required to facilitate the maintenance and the update of the binding. 

## Risks and assumptions

The main risks are:
- The binding is not compatible with all the features of the engine,
- The binding is not as fast as other bindings in other languages,
- The binding is not as easy to use as other bindings in other languages,
- The binding is not as easy to maintain as other bindings in other languages,
- The binding does not respect the laws and regulations required to be used in some industries,
- The binding is not well documented and is confusing for the user,
- The binding is difficult to be maintained and updated,
- The binding is not compatible with the latest version of the engine and is difficult to update.

With all of these concerns, the binding might be deprecated and not used anymore.

To prevent this from happening, the binding needs to be thought and designed in a way that it is easy to maintain and update through the time.  

## Success criteria 

The binding will be considered as a success if it is compatible with all the features of the engine, if it is on the same degree of performance as other bindings in other languages. 

We aim to have a binding useful and adapted for the users and the future needs of the engine.


## Out of scope 

The binding will not be compatible with the version of the engine that are not available on the GitHub repository. 

It can not be fully compatible with the older versions of the engine. 

If the engine receives new features, the binding will not automatically be supported for these versions.

## Glossary

- Binding: a binding is a way to access a library in a different language than the one it was written in. 

- Rust: Rust is a programming language that is designed to be fast, reliable and productive. It is a compiled language that is used to create low level software like operating systems, device drivers, and embedded software. 

- 3D engine: A 3D engine is a software that is used to create 3D applications. It is used to create 3D games, simulations, and data visualization.

- SWIG: SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages.

- Data scientist: A data scientist is a person who is skilled in extracting knowledge or insights from data in various forms, either structured or unstructured, similar to a data analyst but more focused on advanced analysis and modeling techniques.

- AR: Augmented reality is a live direct or indirect view of a physical, real-world environment whose elements are augmented by computer-generated sensory input such as sound, video, graphics or GPS data.

- VR: Virtual reality is a computer technology that uses virtual reality headsets, sometimes in combination with physical spaces or multi-projected environments, to generate realistic images, sounds and other sensations that simulate a user's physical presence in a virtual or imaginary environment.

- ISO 26262: ISO 26262 is an international standard for road vehicles that specifies the functional safety requirements for electrical and/or electronic systems and their software. It is a part of the ISO 26200 series of standards for road vehicles. 

- MISRA: MISRA is an independent organization that provides coding standards for the development of embedded software, that specifies a set of rules for the C and C++ programming languages in order to keep the code consistent and to avoid common programming mistakes.

- AutoSAR: AutoSAR is a set of guidelines for the development of software for automotive electronic control units (ECUs). It is based on the AUTOSAR standard and is used in the automotive industry, however it is not necessary to use it to develop the infotainment system of a car.
