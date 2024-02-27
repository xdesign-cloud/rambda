# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased - Will be: 1.2.0

## 1.1.0
### Added
- Moved `request` variable to be keyword only, and only injected if defined in the destination function.
- Made `@lambda_rest_endpoint` work with non-jwt protected endpoints.


### Fixed
- Fixed bug using `@lambda_rest_endpoint` that prevented the format of `return 200, {}` from being used.