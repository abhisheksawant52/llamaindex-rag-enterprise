# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-08

### Added

- LlamaIndex-based RAG application with a FastAPI service exposing `/health`,
  `/ready`, `/ingest`, `/query`, and `/documents` endpoints.
- Document ingestion and node-parsing pipeline, `VectorStoreIndex` builder, and
  a retriever + response-synthesizer query engine with `similarity_top_k`.
- `RagService` orchestration layer and pydantic request/response models.
- Terraform infrastructure under `terraform/` provisioning an ECR repository,
  S3 bucket for index persistence, CloudWatch log group, and a reusable
  OpenSearch vector-store module, with dev/prod environment configurations.
- Multi-stage Dockerfile (non-root, healthcheck), pytest suite, and
  documentation including an architecture overview.
- Open-source project files: LICENSE (MIT), CONTRIBUTING, SECURITY,
  CODE_OF_CONDUCT, CI workflow, pre-commit hooks, issue/PR templates,
  CODEOWNERS, and Dependabot configuration.
