# GameTracker
This repository contains the database architecture, schema definitions, and analytical queries for a unified, cross-platform video game library and telemetry tracker. Designed entirely in SQLite, this project normalizes highly variable gaming data across distinct hardware ecosystems (PC, Xbox, PlayStation, and Nintendo Switch) into a single, cohesive relational model.

This was developed as a senior database design project to demonstrate advanced data modeling, strict schema enforcement, and the ability to extract actionable business intelligence from heterogeneous data sources.

The Analytical Challenge

A major hurdle in gaming analytics is the inconsistency of telemetry. An achievement on Steam is structurally different from a PlayStation Trophy, and hardware metrics for a desktop PC (e.g., GPU temperature, frame rates) do not translate to handheld consoles.

Instead of relying on a sparse, flat table with dozens of NULL columns, this database solves the problem through:

Deep Normalization: Utilizing a central Game_Ownership junction table to resolve the many-to-many relationship between software titles and hardware platforms.

Dynamic JSON Schemas: Leveraging SQLite's JSON functions to store and query flexible, platform-specific hardware telemetry directly within a relational structure.

Strict Data Integrity: Implementing advanced CHECK constraints to ensure logical consistency (e.g., preventing a "Platinum" tier from being assigned to an Xbox "Gamerscore" achievement).

Technical Stack & Features

Engine: SQLite (Utilizing STRICT tables)

Key SQL Concepts Demonstrated:

Complex Table Joins & Junction Tables

JSON Object Extraction & Querying (json_valid, json_extract)

Multi-column CHECK constraints and Composite UNIQUE keys

Window Functions & Aggregations for time-series session data

Repository Contents

schema.sql: The Data Definition Language (DDL) scripts to generate the tables, constraints, and relationships.

seed_data.sql: (Or a Python Faker script) Generates a large-scale, realistic dataset for analytical querying.

analytical_queries.sql: A collection of advanced queries answering specific business questions (e.g., "What is the average session playtime distribution between handheld and desktop form factors?").

ERD_Diagram.png: The Entity-Relationship diagram mapping the cardinality of the database.
