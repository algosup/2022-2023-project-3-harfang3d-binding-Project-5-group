# Introduction

This document is the test plan for this project. This document will list all the tests made on the project, when they were made and if they were successfull or not.

Author: [Malo Archimbaud](https://github.com/Malo-Archimbaud)

<details>

<summary> Table of content </summary>

- [Introduction](#introduction)
- [1 Glossary](#1-glossary)
- [2 Scope of testing](#2-scope-of-testing)
- [3 Test Strategy](#3-test-strategy)
- [4 Test Environment](#4-test-environment)
- [5 Testing](#5-testing)

</details>

# 1 Glossary

- <ins>FABGen</ins>: FABGen is a set of scripts used to generate bindings with other languages such as Python, Lua and Go.
- <ins>Harfang</ins>: Harfang is a 3D engine developed in C++ and it uses FABGen to have compatibility with other languages.
- <ins>Docker</ins>: Docker is a platform which allows you to build, share and run applications on any platform by emulating everything needed.

# 2 Scope of testing

The goal of the project is to create the binding in Rust for FABGen. There are already some tests for the other languages, so we will translate these tests so that we can use them with Rust. We will also test that the bindings work properly by using Harfand3D in Rust.

All the test provided should pass and we have to be able to use FABGen without crashes to meet our success criteria.

# 3 Test Strategy

The first step will be to pass the tests already provided with FABGen to be sure that our bindings works as intended. 

Then, we will use our bindings to use Harfang3D in Rust and ensure that the engine behaves as it would with languages already supported by FABGen.

We will also let a user unfamiliar with FABGen uses it to ensure that our bindings are easy to use and that they are fairly intuitive.

Any bugs encountered while using the Rust bindings of FABGen will have to be reported on the [issue page](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-5-group/issues) of our github repo

# 4 Test Environment

All the test are going to be run on Mac M1 with the M1 chip. Since the already available tests are not runable on M1 chip and making FABGen compatible is out of scope, we will use Docker to create an image which allow us to run the test.

# 5 Testing

To test if our solution is working as it should, we will use the test that are directly implemented in FABGen. We will also test our solution on some libraries and check if the output is acceptable.