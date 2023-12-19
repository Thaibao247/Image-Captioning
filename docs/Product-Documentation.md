# Product Documentation

## Overview
GitHub serves as an excellent platform for managing and publishing product documentation efficiently. This document outlines the key practices and procedures for handling requirements, storing them as Markdown files within GitHub, and ensuring close integration with the application's source code.

## Docs-as-code
Docs-as-code is an approach to documentation where the documentation lives in source control, often next to the same code it is describing. 
### Keeping code and docs in sync
Keeping documentation separate from code often leads to outdated information, causing confusion and productivity loss. Integrating documentation with code helps developers stay in sync by allowing immediate updates during code changes.

### Writers and developers working together
Especially with complex technical projects developers have to work closely with technical writers to review documentation. Likewise if developers are contributing to documentation, changes will be reviewed by the technical writers.

### Automated checks
As we integrate documentation into our CI/CD pipeline, we can incorporate automated checks to enhance its quality. Clients may prefer receiving documents in PDF format. This requirement involves using tools or scripts to auto convert Markdown files to PDF so that the documentation can be shared with clients in a more traditional format.

## Requirement Management
### Storage and Coupling
Requirements are stored as Markdown files directly within the GitHub repository, establishing a tight coupling between the documentation and the application's source code.

### Creating New Requirements
**Branch Creation:** For every new requirement, a dedicated branch is created with revisions to the product documentation. This can involve either adding a new file or updating an existing one.

**Review and Development:** The newly introduced requirement undergoes a thorough review, development, and testing phase before being committed to the develop branch.

**Tracking Progress:** Progress tracking is facilitated through Jira tickets that are linked to the branch and associated commits.

<img src="requirement-flow.svg" width="100%"/>

## Release Management
### Documentation Generation
By the end of each release, a comprehensive product management overview is generated using a static site generator. This generator can be either Mkdocs or Jekyll, providing a structured and organized representation of the product documentation.

<img src="document-generation.svg" width="100%"/>

### Versioning and Accuracy
GitHub's versioning capabilities play a crucial role in ensuring the accuracy of each release's documentation. The platform provides an audit trail that captures differences between versions, contributing to a reliable and transparent documentation process. Reference to [Version control systems](https://idratherbewriting.com/learnapidoc/pubapis_version_control.html)

## Conclusion
In conclusion, leveraging GitHub for product documentation offers a robust and streamlined approach. The integration of requirements with source code, coupled with efficient versioning and release management, enhances collaboration and ensures the integrity of the documentation throughout the development lifecycle.


## References
[I’d Rather Be Writing - Docs as code](https://idratherbewriting.com/learnapidoc/pubapis_docs_as_code.html)

[Quick Start with Docs as Code](https://www.docslikecode.com/)

[Version control systems](https://idratherbewriting.com/learnapidoc/pubapis_version_control.html)