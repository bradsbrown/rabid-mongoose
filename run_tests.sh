#!/bin/bash

pytest --gherkin-terminal-reporter --gherkin-terminal-reporter-expanded -vv "$@"
