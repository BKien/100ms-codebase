# Prompts contract

## Configured prompt template

Follow the [configured template](../../../../templates/construction/coding-prompt.template.md) for the complete prompt. Its sections, order and instructions define the prompt structure.

Raw UC success fields become the domain payload in the standard success envelope; UC error status/message use the standard error envelope. This transport normalization must not change business meaning.

The configured DBML is shared technical input wherever required by the configured template or applicable input contract. Apply the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution) and existing database preflight.
