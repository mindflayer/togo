# Copilot Instructions for ToGo

## Project Overview

ToGo is a high-performance Python library for computational geometry, providing Cython bindings for the [TG](https://github.com/tidwall/tg) C library and integrating with [GEOS](https://libgeos.org/) for advanced operations. The project focuses on fast point-in-polygon operations and efficient geometric computations.

## Technology Stack

- **Language**: Python 3.8+ with Cython 3.0+
- **Core Dependencies**: 
  - Cython for C bindings
  - TG and TGX C libraries (vendored)
  - GEOS library (built from source, vendored)
- **Build System**: setuptools with Cython compilation
- **Testing**: pytest
- **Formatting**: ruff (formatter and linter)
- **Pre-commit**: Multiple hooks including cython-lint

## Building and Testing

### Build Commands

```bash
# Install dependencies and build
make install-deps  # Sets up venv and downloads TG/TGX sources
make build         # Builds wheel package

# Test
make test          # Runs pytest

# Benchmarks
make bench         # Runs benchmarks against Shapely
```

### Key Build Details

1. **Vendor Dependencies**: The project vendors GEOS library. The script `tools/prepare_vendor.sh` downloads and builds GEOS from source for the current platform.
2. **TG/TGX Sources**: Downloaded by `tools/prepare_tg.py` from GitHub repos.
3. **Platform-specific Builds**: GEOS is built per-platform (identified by `CIBW_BUILD` env var or 'local').
4. **Static Linking**: GEOS libraries (`libgeos.a`, `libgeos_c.a`) are statically linked using `--whole-archive`.

### Running Tests

- Use `make test` or directly `.venv/bin/pytest`
- Tests are in `tests/` directory
- Test configuration is in `pyproject.toml` under `[tool.pytest.ini_options]`

## Code Style and Conventions

### Python Code

- **Formatter**: Use `ruff format` for Python code
- **Linter**: Use `ruff` with auto-fix enabled
- **Line Length**: 100 characters (configured in `pyproject.toml`)
- **Imports**: Standard Python import ordering

### Cython Code

- **Line Length**: Maximum 100 characters (configured in `[tool.cython-lint]`)
- **String Quotes**: Use double quotes for Cython strings (enforced by pre-commit hook)
- **Language Level**: Python 3 (`# cython: language_level=3` at top of `.pyx` files)
- **Type Declarations**: Use Cython's `cdef` declarations for C types

### Testing Conventions

- Use `pytest` for all tests
- Test files follow `test_*.py` naming convention
- Test classes start with `Test` prefix
- Test functions start with `test_` prefix
- Use descriptive test names that explain what is being tested
- Example test structure:

```python
def test_geometry_wkt():
    g = Geometry("POINT(1 2)", fmt="wkt")
    assert g.type_string() == "Point"
    assert g.to_wkt() == "POINT(1 2)"
```

### API Design Patterns

1. **Dual API**: The project provides both original ToGo API and Shapely-compatible API
2. **Geometry Wrapping**: Python classes wrap C structures using Cython
3. **Format Support**: WKT, GeoJSON, WKB, and HEX formats for geometry I/O
4. **Spatial Predicates**: Methods like `contains()`, `intersects()`, `touches()`, etc.
5. **As-Conversion**: Use `as_geometry()` to convert Python geometry objects to base `Geometry` class

## Development Workflow

### Pre-commit Hooks

The repository uses pre-commit hooks (`.pre-commit-config.yaml`):
- CRLF/trailing whitespace checks
- TOML/YAML validation
- Ruff formatting and linting
- Cython linting

Run hooks manually: `pre-commit run --all-files`

### CI/CD

- **Testing**: GitHub Actions workflow `python-tests.yml` tests against Python 3.8-3.14
- **Wheel Building**: `build-wheels.yml` builds platform-specific wheels
- **GEOS Caching**: CI caches built GEOS libraries to speed up builds

## Important Notes for Code Changes

### When Modifying Cython Code

1. **Memory Management**: Be careful with C memory allocation/deallocation
   - Use `tg_geom_free()`, `tg_ring_free()`, etc. to free C structures
   - Consider ownership semantics (clone vs. copy)

2. **Type Conversions**: 
   - Convert between Python and C types explicitly
   - Handle NULL pointers and error conditions
   - Check for errors using `tg_geom_error()`

3. **Building**: After changing `.pyx` files, rebuild with `make build`

### When Adding New Features

1. **Maintain Dual API**: Consider both ToGo and Shapely-compatible APIs
2. **Add Tests**: Write tests for new functionality in appropriate `test_*.py` file
3. **Update Documentation**: Update README.md or API documentation files if needed
4. **Format Code**: Run pre-commit hooks before committing

### When Adding Dependencies

1. **Python Dependencies**: Add to `requirements.txt`
2. **Build Dependencies**: Update `pyproject.toml` `[build-system]` section
3. **C Libraries**: Vendor them similar to GEOS if needed

### Security Considerations

- This project handles memory at the C level - be vigilant about:
  - Buffer overflows
  - Memory leaks
  - Use-after-free errors
- Run with AddressSanitizer in development: `ASAN=1 make build`

## Project Structure

```
togo/
├── .github/          # GitHub workflows and configurations
├── benchmarks/       # Performance benchmarks
├── examples/         # Usage examples
├── tests/            # Test suite
├── tools/            # Build and vendor scripts
├── vendor/           # Vendored GEOS libraries (generated)
├── togo.pyx          # Main Cython source file
├── setup.py          # Build configuration
├── pyproject.toml    # Project metadata and tool configs
└── README.md         # User documentation
```

## Common Tasks

### Adding a New Geometry Operation

1. Add Cython function wrapper in `togo.pyx` that calls TG C function
2. Add method to appropriate Python class (Point, Line, Ring, Poly, Geometry)
3. Write tests in corresponding `test_*.py` file
4. Update README with usage example if public API

### Debugging Build Issues

1. Check that vendor dependencies are built: `ls -la vendor/geos/local/`
2. Verify TG sources downloaded: `ls -la tg.h tg.c tgx.h tgx.c`
3. Clean and rebuild: `make clean && make build`
4. Check build logs for C compilation errors

### Running Specific Tests

```bash
.venv/bin/pytest tests/test_geometry.py::test_geometry_wkt -v
.venv/bin/pytest tests/test_buffer.py -v
```

## References

- [TG Library](https://github.com/tidwall/tg) - Core C geometry library
- [TGX Extension](https://github.com/tidwall/tgx) - GEOS integration
- [GEOS](https://libgeos.org/) - Geometry Engine Open Source
- [Shapely](https://shapely.readthedocs.io/) - Inspiration for compatible API
