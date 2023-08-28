#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import Architect, Engineer, ProductManager, ProjectManager, QaEngineer
from metagpt.software_company import SoftwareCompany


async def startup(idea: str, investment: float = 3.0, n_round: int = 5,
                  code_review: bool = True, run_tests: bool = False):
    """Run a startup. Be a boss."""
    company = SoftwareCompany()
    company.hire([ProductManager("Abe"),
                  Architect("Darwin"),
                  ProjectManager("John"),
                  Engineer("Alex", n_borg=5, use_code_review=code_review),
                  QaEngineer("Olga")])
    if run_tests:
        # developing features: run tests on the spot and identify bugs (bug fixing capability comes soon!)
        company.hire([QaEngineer()])
    company.invest(investment)
    company.start_project(idea)
    await company.run(n_round=n_round)


def main(idea: str, investment: float = 20.0, n_round: int = 5, code_review: bool = False, run_tests: bool = False):
    """
    We are a software startup comprised of AI. By investing in us, you are empowering a future filled with limitless possibilities.
    :param idea: Your innovative idea, such as "Creating a snake game."
    :param investment: As an investor, you have the opportunity to contribute a certain dollar amount to this AI company.
    :param n_round:
    :param code_review: Whether to use code review.
    :return:
    """
    if True:
        idea = '''
            Design a Prompt Gateway System for an LLM (Large Language Model) with the following features:
            1. The way of Access: The Prompt Gateway implements the RESTful API via a specific URL with swagger support.
            2. Prompt Input: The System should allow API Callers to provide initial Prompts.
            3. Plugins: Implement plugins to transform prompts.
            4. Plugins Chaining: Plugins can be chained in the specific order, so prompt gets transformed by each Plugin
               and the result goes to the next plugin or, finally, to the Prompt Gateway.
            5. Plugin Representation: Plugins can be third-party RESTful API endpoints.
            6. Error Handling: Implement Logging for errors and exceptions.
               In case of Failures, the System should automatically Retry the execution to ensure Reliability.
            7. Testing: Include Unit Testing and Integration Tests.
            8. Documentation: Create detailed Documentation for the Prompt Gateway system.
               Include instructions for using the Gateway, configuring plugins,
               and troubleshooting potential issues.
            9. Create example plugin.
            '''
        idea = '''
            Design a Prompt Gateway System for an LLM (Large Language Model) with the following features:
            1. The Prompt Gateway implements the RESTful API via a specific URL.
            2. The Prompt Gateway enables swagger page.
            3. The System should allow API Callers to provide initial Prompts.
            4. Implement chainable plugins to transform prompts.
            5. Implement Logging for errors and exceptions.
            6. Handle failures by retries to ensure Reliability.
            7. Testing: Include Unit Testing and Integration Tests.
            8. Create documentation. Include configuration and usage instructions.
            '''
        idea = '''
            Design a Prompt Gateway System for an LLM (Large Language Model) with the following features:
            1. The way of Access: The Prompt Gateway should be accessible through the RESTful API via a specific URL.
            1. Prompt Input: The System should allow API Callers to provide Prompts, which will be used as the initial text for processing.
            2. Plugin Chaining: Implement a mechanism to apply a Chain of Plugins to the initial Prompt. Each plugin will transform the
               Prompt in a specified order, with the output of one Plugin serving as the input for the next.
            3. Plugin Representation: Represent each plugin as a REST endpoint accessible via a specific URL. Plugins should be hosted independently,
               and the Prompt Gateway will interact with them using standard HTTP Methods.
            4. Plugin Configuration: The Plugins will be configured independently at their Hosts. The Prompt Gateway will not handle internal configurations,
               ensuring flexibility and modularity.
            5. Use async/await wherever it does make sense.
            5. Error Handling: Implement Logging for errors and exceptions during the Transformation Process. In case of Failures, the System should
               automatically Retry the execution to ensure Reliability.
            6. Testing: Develop a comprehensive Testing Strategy to verify the Correctness and Reliability of the Prompt Gateway. Include Unit Testing and
               Integration Testing to ensure the chaining of Plugins and Transformations work as expected.
            7. Create startup shell script to run locally. 
            8. Create ansible script for deployment. 
            9. Documentation: Create detailed Documentation for the Prompt Gateway system. Include instructions for using the Gateway, configuring plugins,
               and troubleshooting potential issues. Use markdown (.md) format for the documentation.
            '''
        idea = '''
            Create a Prompt Gateway for an external LLM with these specifications:
            - Prompt Gateway is accessible to clients via a specific RESTful API URL.
            - Prompt gateway reliably accepts prompts, then applies optional transformations, and sends transformed prompts to the LLM.
            - Prompt Gateway handles Prompt Transformations via any number of external and/or internal Plugin modules.
            - Prompt Gateway uses an internal rule engine to determine the order of the Prompt Transformations by the Plugins.
            - An Admin can configure the Prompt Gateway with any number of Plugins.
            - Prompt Transformation Plugins are accessible to the Prompt Gateway only via their respective RESTful endpoint URLs.
            
            Provide a local startup shell script.
            Create deployment artifacts for Ansible and Docker.
            Produce comprehensive documentation: usage, plugin configuration, and troubleshooting.
            '''
    code_review = True
    run_tests = True
    asyncio.run(startup(idea, investment, n_round, code_review, run_tests))


if __name__ == '__main__':
    fire.Fire(main)
