# d42-cf_templates
  - [1. Description](#1-description)
  - [2. Features](#2-features)
  - [3. Requirements](#3-requirements)
  - [4. How to Use](#4-how-to-use)
    - [4.1. cd to d42-cf_templates and Create a new virtualenv](#41-cd-to-d42-cf_templates-and-create-a-new-virtualenv)
    - [4.2. Activate the virtual environment](#42-activate-the-virtual-environment)
    - [4.3. Install requirements](#43-install-requirements)
    - [4.4. Rename config.yaml.example to config.yaml and fill out the required fields](#44-rename-configyamlexample-to-configyaml-and-fill-out-the-required-fields)
    - [4.5. Replace example templates in templates.yaml with your own](#45-replace-example-templates-in-templatesyaml-with-your-own)
    - [4.6. Run](#46-run)
    - [4.7. Schedule via cron](#47-schedule-via-cron)
  - [5. How it Works](#5-how-it-works)
    - [5.1. Example template:](#51-example-template)
  - [6. Example Output](#6-example-output)

## 1. Description
Quick way to define templates to create application components for apps that Device42 does not support out of the box and pin/star services accordingly.

## 2. Features
- Automatically pin / set topology status for service instances matching on name or cmd path args.
- Automatically create application component records on devices with associated service instances

## 3. Requirements
- Python 3.6.9 or > 
    - PyYAML==5.4.1
    - requests==2.25.1
- Device42 MA 16.22.00.1612807182 or >

## 4. How to Use
### 4.1. cd to d42-cf_templates and Create a new virtualenv 

    venv venv

OR

    python3 -m venv venv



### 4.2. Activate the virtual environment

    source venv/bin/activate

### 4.3. Install requirements

    pip install -r requirements.txt

### 4.4. Rename config.yaml.example to config.yaml and fill out the required fields

### 4.5. Replace example templates in templates.yaml with your own

### 4.6. Run 

    python starter.py

### 4.7. Schedule via cron
In crontab add a line like the following to set your command execution schedule:

    0 0 * * * python /home/your_user_here/d42-apptemplates/starter.py

This will run the script every night at midnight.

## 5. How it Works
### 5.1. Example template:

    Building_Metadata_WH: -- This is the name of the custom field template
        ci_type: 'building' -- The CI type {Building, room, rack, device, asset, part, appcomp}
        unique_id: 'building_pk' -- The name of the primary key
        saved_doql: 'All_Buildings' -- The name of a Saved DOQL Query in your Device42 instance
        custom_fields: -- Define a list of custom fields here
            Building Owner: -- This is the custom field key
            type: 'text' -- Data type
            value: 'Dwight Schrute' -- Value of the custom field
            filterable: 'yes' -- Set to no/yes to allow filtering of field in the UI

In the above example, the script will query Device42 for a saved doql query with the name 'All_Buildings'. It will then iterate through all rows in the response data, creating/updating a custom field for each row.

## 6. Example Output
Below is sample output returned from executing the script:  

        Loading template: Building_Metadata_WH

        Calling saved DOQL query: All_Buildings

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Dwight Schrute', 'filterable': 'yes', 'id': 168, 'key': 'Building Owner'}
                Response: {'msg': ['custom key pair values added or updated', 168, 'Narnia', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Michael Scott', 'filterable': 'yes', 'id': 168, 'key': 'Building Manager'}
                Response: {'msg': ['custom key pair values added or updated', 168, 'Narnia', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Dwight Schrute', 'filterable': 'yes', 'id': 170, 'key': 'Building Owner'}
                Response: {'msg': ['custom key pair values added or updated', 170, 'West Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Michael Scott', 'filterable': 'yes', 'id': 170, 'key': 'Building Manager'}
                Response: {'msg': ['custom key pair values added or updated', 170, 'West Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Dwight Schrute', 'filterable': 'yes', 'id': 1, 'key': 'Building Owner'}
                Response: {'msg': ['custom key pair values added or updated', 1, 'New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/building/
                Payload: {'type': 'text', 'value': 'Michael Scott', 'filterable': 'yes', 'id': 1, 'key': 'Building Manager'}
                Response: {'msg': ['custom key pair values added or updated', 1, 'New Haven', False, False], 'code': 0}

        Loading template: Room_Metadata_WH

        Calling saved DOQL query: All_Rooms

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 3, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 3, 'IDF3 @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 2, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 2, 'IDF2 @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 1, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 1, 'NHDC1 @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 46, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 46, 'Transit @ West Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 5, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 5, 'IT Lab @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 20, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 20, 'wardrobe @ Narnia', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 26, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 26, 'IDF2 @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 28, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 28, 'QTS demo room @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 42, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 42, 'QA LAb @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 21, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 21, 'WH01 @ West Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 6, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 6, 'Corner Room @ New Haven', False, False], 'code': 0}

        Put: /api/1.0/custom_fields/room/
                Payload: {'type': 'text', 'value': '30', 'filterable': 'yes', 'id': 4, 'key': 'Circuit Amperage'}
                Response: {'msg': ['custom key pair values added or updated', 4, 'IDF4 @ New Haven', False, False], 'code': 0}