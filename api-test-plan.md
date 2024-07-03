Test plan for a flask-app

Application Overview

The Flask API backend serves as a robust automation platform for video
generation, designed to streamline and enhance the process through a
suite of RESTful endpoints. The application\'s key functionalities
include comprehensive CRUD operations for managing entities such as
users, projects, scripts, audio files, images, and renders.

-   **Script Generation:** Utilizes ChatGPT for generating scripts based
    on predefined themes or project requirements.
-   **Image Generation:** Employs DallE for creating images that
    complement the generated scripts and project themes.
-   **Rendering Capabilities:** Offers functionalities for generating
    slideshows, incorporating voiceovers generated via OpenAI\'s
    text-to-speech (TTS) service, and adding subtitles using the ZapCap
    API.

The backend architecture is structured into distinct layers:

-   **API Layer:** Implements RESTful endpoints using Flask,
    facilitating intuitive interaction with the application\'s
    functionalities.
-   **Service Layer:** Houses the business logic responsible for
    orchestrating AI-based content generation and integrating external
    APIs for additional functionalities.
-   **Repository Layer:** Manages database operations, ensuring
    efficient storage and retrieval of project-related data.

Scope of Testing

Modules to be Tested:

1.  **API Layer:**

    -   Flask endpoints responsible for CRUD operations (users,
        projects, scripts, audio, images, renders).
    -   Integration with AI services (ChatGPT for script generation,
        DallE for image generation, OpenAI TTS for voiceovers).
    -   Integration with third-party APIs (ZapCap for subtitles).

2.  **Service Layer:**

    -   Business logic for orchestrating AI-based functionalities.
    -   Script generation based on themes or project requirements.
    -   Image generation to complement generated scripts and project
        themes
    -   Rendering capabilities of in-house movie editor service.

3.  **Repository Layer:**

    -   Database operations for storing and retrieving data related to
        users, projects, scripts, etc.

Modules Not to be Directly Tested:

-   External AI services (ChatGPT, DallE, OpenAI TTS, ZapCap): These
    services are assumed to be tested and functioning correctly by their
    respective providers. Our testing will focus on integration points
    and handling of responses.

Testing Approaches and Methodology

**Approach:** Our testing approach integrates both traditional and
modern methodologies to ensure comprehensive coverage and reliability of
the Flask API backend. We emphasize:

-   **Agile Testing:** Iterative testing throughout development cycles
    to catch issues early.
-   **TDD:** In case of post-MVP (Minimum Viable Product) feature
    development the testing practice should follow steps defined by TDD.
-   **Continuous Integration/Continuous Deployment (CI/CD):** Automated
    testing integrated into CI/CD pipelines for rapid feedback and
    deployment assurance. Including static code analysis, quality gates
    should be well defined.

Methodology:

-   **Risk-based Testing:** Prioritizing tests based on potential impact
    and likelihood of failure.
-   **Exploratory Testing:** Manual testing to uncover unforeseen issues
    and ensure usability.
-   **Test Automation:** Using frameworks like pytest for automated
    testing to improve efficiency and consistency.

#### []{#anchor}

#### []{#anchor-1}Types of Testing

  --------------------- ---------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------
  Functional Testing    Objective                                                                                            Criteria
  Unit Testing          Validate individual components (functions, methods, classes).                                        High code coverage (80%+) for critical paths. Mock external dependencies (AI services, third-party APIs) to maintain test independence.
  Integration Testing   Validate interactions between components (API, services, repository).                                Test data flow and transformations across layers. Verify error handling and edge case scenarios.
  Contract Testing      Validate responses from third party APIs.                                                            Define data transfer objects and test API response structure.
  End-to-End Testing    Validate complete user workflows from API request to final output (rendered video). Ex. pytest-bdd   Test user scenarios including script generation, image rendering, and final render creation.
  --------------------- ---------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------

+----------------------+----------------------+----------------------+
| Non-Functional       | Objective            | Criteria             |
| Testing              |                      |                      |
+----------------------+----------------------+----------------------+
| Performance Testing  | Identify performance | Define performance   |
|                      | bottlenecks and      | metrics (e.g.,       |
|                      | optimize system      | response time \<     |
|                      | performance.         | 500ms).              |
|                      |                      |                      |
|                      | Ex. locust           |                      |
+----------------------+----------------------+----------------------+
| Security Testing     | Identify and         | Scan dependencies    |
|                      | mitigate security    | and third party      |
|                      | vulnerabilities.     | libraries for        |
|                      |                      | security issues.     |
|                      | Ex. pip-audit        |                      |
+----------------------+----------------------+----------------------+
| Penetration Testing  | Assure the           | Test for security    |
|                      | robustness and       | breaches through     |
|                      | security of our API. | API's endpoints.     |
|                      |                      |                      |
|                      | Ex. ZAP              |                      |
+----------------------+----------------------+----------------------+

Test Schedule and Timeline

** **A static code analysis tool should get included into the project's
git flow as a github action, to ensure that the codebase is compliant
with modern python coding standards.

** **Functional testing should be done first, focusing from most
critical to least critical parts of the codebase. After identifying such
a critical code part, unit tests should pass, following that we can
integrate the unit tested parts and test cross-module work flows. During
integration with a third party library contract tests should be defined
and maintained as border tests, to alert any changes of external APIs.
Following these steps complete user workflows should get tested in a BDD
manner. Gherkin is offered by pytest-bdd to define expected behaviors.

Once functional testing ensures our minimum viable product to meet
defined criterias, security and penetration testing should get included
into our pipelines.

Before the release of a beta version performance testing should validate
our response times.

Testing convention

** **During functional testing, the implementation in pytest should
follow integration conventions described in the original documentation:
https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html

**Identified Risks**

**Resource Constraints:** Limited availability of testing resources
(e.g., time, personnel) may delay testing activities.

**Integration Complexity:** Complex integrations between API endpoints,
AI services, and third-party APIs may result in integration failures.

**ZapCap development: **The third party API used for subtitle generation
is in alpha version, meaning it is still under development and can be
subject to drastic changes. The development process and detailed
explanations are available on their Discord server, it is advised to
monitor them.

#### []{#anchor-2}**Mitigation Strategies**

1.  -   Establish regular checkpoints to monitor test progress and
        identify potential bottlenecks early.
    -   Develop contingency plans for identified risks to minimize
        impact on testing timelines.
    -   Maintain flexibility in testing schedules to accommodate
        unexpected delays or issues.
    -   Ensure testing team members are adequately trained in testing
        methodologies and tools.
