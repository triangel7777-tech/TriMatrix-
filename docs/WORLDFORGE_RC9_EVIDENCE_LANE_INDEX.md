# World-Forge RC9 Evidence Lane Index

This file consolidates the two remaining evidence lanes.

## Lane A: workflow run evidence

Required:

- repository name
- workflow name
- workflow run ID
- workflow run URL
- job list
- job logs
- artifact name
- artifact checksum
- parsed promotion report

## Lane B: independent review evidence

Required:

- reviewer handle
- independence statement
- reviewed run ID
- reviewed artifact checksum
- review result
- public reference or signature
- review timestamp

## Gate rule

A final packet can be marked review-ready only when Lane A and Lane B are complete.

The system must report missing evidence directly and must not promote beyond the imported evidence.

## Current missing evidence

- workflow run ID
- jobs and logs
- verifier artifact
- parsed promotion report
- approved independent review
