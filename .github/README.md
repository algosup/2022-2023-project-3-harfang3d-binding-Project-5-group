# 2022-2023-project-3-harfang3d-binding-Project-5-group

## Documents 

- [Functional Specification](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-5-group/blob/documents/documents/Functionnal%20Specifications.md)
- [Technical Specification](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-5-group/blob/documents/documents/Technical%20Specifications.md)

## Project Team

| Members         | Roles             |
| --------------- | ----------------- |
| Victor LEROY    | Project Manager   |
| Clémentine CUREL| Tech Lead         |
| Théo DIANCOURT  | Program Manager   |
| Paul MARIS      | Software Engineer |
| Malo ARCHIMBAUD | Quality Assurance |

# Development

### Test the binding (Rust)

`python3 bind.py --rust --out ./output/bind_dev test_bind.py`

### Update Harfang3D version

`git submodule update --remote --merge`

### Tests

- Unix:
    1. `make build`
    2. `make tests-all`

- Windows:
    1. `wsl`
    2. `make build`
    3. `make tests-all`