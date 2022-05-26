# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [dev] - unreleased
### Added
### Changed
- replaced asserts with `ValueError` as asserts can be disabled. [#91](https://github.com/RECETOX/RIAssigner/pull/91)
- updated matchms dependency to `>= 0.14.0`. [#90](https://github.com/RECETOX/RIAssigner/pull/90)
### Removed
- removed test cases which include data that has `None` retention times. [#90](https://github.com/RECETOX/RIAssigner/pull/90)

## [0.3.2] - 2022-02-11
### Added
- data/Data.py: Added `update_possible_rt_keys()` and `update_possible_ri_keys()` methods for `Data` class.
Now users can supply their own identifiers for RT/RI columns (csv files) and identifiers (msp) in their data. [#74](https://github.com/RECETOX/RIAssigner/pull/74)
- General: Added missing documentation and updated [README](README.md). [#80](https://github.com/RECETOX/RIAssigner/pull/80)
- setup.py: Added versions for dependencies. [#80](https://github.com/RECETOX/RIAssigner/pull/80)
- utils.py: Added method to check if array is sorted. [#82](https://github.com/RECETOX/RIAssigner/pull/82)
- data/SimpleData.py: Added class for in-memory data which is read-only. [#82](https://github.com/RECETOX/RIAssigner/pull/82)
### Changed
- data/Data.py: Unified default RT/RI column identifiers between `PandasData` and `MatchMSData` classes. [#74](https://github.com/RECETOX/RIAssigner/pull/74)
- data/MatchMSData.py: `MatchMSData` class now looks up for RT and RI identifiers from within default identifiers list
instead of hardcoded 'retentiontime' & 'retentionindex' keys. [#74](https://github.com/RECETOX/RIAssigner/pull/74)
- compute/Kovats.py: Computation is now real piece-wise linear interpolation and doesn't assume a step width of 100 but interpolates in the actual interval. [#76](https://github.com/RECETOX/RIAssigner/pull/76)
### Removed
- data/Data.py: Removed `read` method from class and contructor -> all child classes must now explicitly implement and call the superclass constructor. [#82](https://github.com/RECETOX/RIAssigner/pull/82)

## [0.3.1] - 2021-12-9
### Changed
- data/PandasData.py: `_read_into_dataframe()` now deduces a proper delimiter via Python's [`csv.Sniffer`](https://docs.python.org/3/library/csv.html#csv.Sniffer) class. [#73](https://github.com/RECETOX/RIAssigner/pull/73)

## [0.3.0] - 2021-09-03
### Added
- __main__.py + cli/LoadDataAction.py: Added required passing of filetype and rt unit. [#64](https://github.com/RECETOX/RIAssigner/issues/64) [#67](https://github.com/RECETOX/RIAssigner/issues/67) [#68](https://github.com/RECETOX/RIAssigner/pull/68)
### Changed
- utils.py: `get_extension` function now returns extension without `.` [#68](https://github.com/RECETOX/RIAssigner/pull/68)
- data/Data.py: Added `filetype` to constructor and made `rt_unit` non-optional. [#67](https://github.com/RECETOX/RIAssigner/issues/67) [#68](https://github.com/RECETOX/RIAssigner/pull/68)
- data/MatchMSData.py: Added `filetype` to constructor and made `rt_unit` non-optional. [#67](https://github.com/RECETOX/RIAssigner/issues/67) [#68](https://github.com/RECETOX/RIAssigner/pull/68)
- data/PandasData.py: Added `filetype` to constructor and made `rt_unit` non-optional. [#67](https://github.com/RECETOX/RIAssigner/issues/67) [#68](https://github.com/RECETOX/RIAssigner/pull/68)

## [0.2.0] - 2021-08-18
### Added
- Added `__eq__` to `PandasData` and `MatchMSData` [#51](https://github.com/RECETOX/RIAssigner/pull/51)
- Added `__eq__` to `ComputationMethod` class and subclasses [#52](https://github.com/RECETOX/RIAssigner/pull/52)
- data/PandasData.py: Added reading `tsv` files. [#49](https://github.com/RECETOX/RIAssigner/pull/49)
- Command line interface functionality [#29](https://github.com/RECETOX/RIAssigner/pull/55)
  - utils.py: `get_extension` function
  - tests/fixtures/data.py: Added `load_test_file` function
### Changed
- data/MatchMSData.py: `_assign_ri_value` now converts all values to float and stores them as string in metadata field
- data/MatchMSData.py `_read_retention_indices` now calls retention_indices property setter to store values
- tests/fixtures/data.py: Changed loading of test data
- compute/CubicSpline.py: `compute` now returns an array of floats [#61](https://github.com/RECETOX/RIAssigner/pull/61)
- compute/Kovats.py: `compute` now returns a list of floats [#61](https://github.com/RECETOX/RIAssigner/pull/61)

## [0.1.0] - 2021-07-12
### Added
- Reading data from `CSV` and `MSP` files [#8](https://github.com/RECETOX/RIAssigner/pull/8)[#15](https://github.com/RECETOX/RIAssigner/pull/15)[#36](https://github.com/RECETOX/RIAssigner/pull/36)
- Computing Kovats retention index [#25](https://github.com/RECETOX/RIAssigner/pull/25)
- Computing RI based on cubic splines [#33](https://github.com/RECETOX/RIAssigner/pull/33)
- Added CI actions to GitHub [#43](https://github.com/RECETOX/RIAssigner/pull/43)
- Added writing data back to memory for `MSP`, `CSV` and `tsv` files [#7](https://github.com/RECETOX/RIAssigner/pull/7)[#14](https://github.com/RECETOX/RIAssigner/pull/14)[#19](https://github.com/RECETOX/RIAssigner/pull/19)
