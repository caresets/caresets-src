# Proposed model-to-glossary mappings

- Generated: 2026-08-29
- Target: append to `input/glossary_mappings.csv` (currently 37 rows over 4 models)
- Proposed: **110** rows over 30 models (**32** rows are in draft models)

Nothing has been written yet. Column 2 is the ElementSuffix, matched by `endswith("."+suffix)`.


## `StructureDefinition-BeModelAnnex81.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date of encoding of the information by the Recorder. |
| `author` | **Recorder** | The person who encodes the prescription (e.g. a doctor, nurse, midwife |
| `status` | **Status** | Is the status of the referral prescription (e.g. planned, complete, st |
| `patient` | **Patient** | The patient's identification. The unique identifier must be the Nation |

## `StructureDefinition-BeModelAssignment.json`

| Element | Glossary code | Model says |
|---|---|---|
| `status` | **Status** | Status of the task |
| `performer` | **Performer** | Information about the intended performer of the task |

## `StructureDefinition-BeModelBodySite.json`

| Element | Glossary code | Model says |
|---|---|---|
| `bodyLocation` | **BodyLocation** | Code that identifies the anatomical location of the specimen on the su |
| `bodyLaterality` | **BodyLaterality** | The laterality of a body site - the side of the body |
| `bodyTopography` | **BodyTopography** | The topography of the location of the specimen on the subject's body |

## `StructureDefinition-BeModelCarePlan.json`

| Element | Glossary code | Model says |
|---|---|---|
| `category` | **Category** | Type of plan |
| `partOf` | **PartOf** | Care plans that this care plan is part of |
| `status` | **Status** | status of the care plan |
| `author` | **Recorder** | Who is responsible for plan |
| `note` | **Note** | Comments about the care plan |

## `StructureDefinition-BeModelCareTeam.json`

| Element | Glossary code | Model says |
|---|---|---|
| `category` | **Category** | Type of team |
| `status` | **Status** | Status of the care team |
| `note` | **Note** | Additional notes |

## `StructureDefinition-BeModelClinicalObservation.json`

| Element | Glossary code | Model says |
|---|---|---|
| `performer` | **Performer** | The professional that performed the observation |
| `device` | **UsedDevice** | The device used to generate the observation data |
| `category` | **Category** | A code that classifies the general type of observation being made |
| `code` | **Code** | Describes what was observed. Sometimes this is called the observation  |
| `status` | **Status** | The status of the result value. |
| `note` | **Note** | Comments about the observation or the results |

## `StructureDefinition-BeModelDocument.json`

| Element | Glossary code | Model says |
|---|---|---|
| `status` | **Status** | Status |
| `author` | **Recorder** | Author(s) |

## `StructureDefinition-BeModelGoal.json`

| Element | Glossary code | Model says |
|---|---|---|
| `category` | **Category** | Category of goal |
| `status` | **Status** | Status of the goal |

## `StructureDefinition-BeModelMedication.json`

| Element | Glossary code | Model says |
|---|---|---|
| `status` | **Status** | Status of the medication (active, inactive, etc.) |
| `code` | **Code** | Code for the medication that is actually being specified. This can be  |
| `batch.lotNumber` | **LotNumber** | Batch number |

## `StructureDefinition-BeModelMedicationDispense.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | The date (or date+time) when the dispense was recorded |
| `patient` | **Patient** | The person for which the medication is dispensed |
| `status` | **Status** | The status of the dispense record |
| `note` | **Note** | Additional information about the dispense - this can be relevant histo |

## `StructureDefinition-BeModelMedicationLine.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Timestamp the medication line content was recorded or last updated. |
| `recorder` | **Recorder** | Recorder |
| `patient` | **Patient** | Patient |
| `status` | **Status** | Status of the line entry |
| `note` | **Note** | A note captured by a professional |

## `StructureDefinition-BeModelMedicationPrescription.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Time of authoring the prescription/draft in the information system |
| `patient` | **Patient** | The person for whom the medication is prescribed/ordered |
| `status` | **Status** | Status of the prescription, this should not be status of treatment |
| `note` | **Note** | Additional information or comments |

## `StructureDefinition-BeModelOrganisationClaim.json`

| Element | Glossary code | Model says |
|---|---|---|
| `status` | **Status** | Status of the task |

## `StructureDefinition-BeModelPatientWill.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date of encoding of the information |
| `patient` | **Patient** | Is the patient's unique identifier. The unique identifier must be the  |
| `recorder` | **Recorder** | Is the unique identifier of either the healthcare professional respons |
| `category` | **Category** | Type of patient wishes. |
| `note` | **Note** | Comments |

## `StructureDefinition-BeModelPopulationScreening.json`

| Element | Glossary code | Model says |
|---|---|---|
| `patient` | **Patient** | The patient for the screening |

## `StructureDefinition-BeModelPopulationScreeningPlan.json`

| Element | Glossary code | Model says |
|---|---|---|
| `patient` | **Patient** | The patient for the screening |

## `StructureDefinition-BeModelProcedure.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date of the last modification/recording of the procedure |
| `patient` | **Patient** | The patient that is the subject of the procedure. |
| `recorder` | **Recorder** | Person, organization or device that recorded the procedure. |
| `performer` | **Performer** | Person who performed the procedure. |
| `partOf` | **PartOf** | Part of the event being referenced: procedure, observation (symptoms)  |
| `category` | **Category** | Type or nature of the procedure. For example: surgical, psychiatric or |
| `usedDevice` | **UsedDevice** | Devices or materials used temporarily during the procedure. For exampl |
| `status` | **Status** | Procedure status (not-done, stopped, completed, entered-in-error). Not |
| `code` | **Code** | Identification of the procedure (SNOMED-CT Procedure concept) |
| `note` | **Note** | Additional information about the procedure |

## `StructureDefinition-BeModelRadiologyPrescription.json`

| Element | Glossary code | Model says |
|---|---|---|
| `bodyLaterality` | **BodyLaterality** | Laterality of the anatomical location where the treatment should be ap |

## `StructureDefinition-BeModelReferralPrescription.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date of recording of the information by the Recorder. |
| `patient` | **Patient** | Identification of the patient. The unique identifier must be: NISS, Na |
| `author` | **Recorder** | The person who encodes the prescription (e.g. a doctor, nurse, midwife |
| `status` | **Status** | Is the status of the referral prescription (e.g. planned, complete, st |
| `bodyLocation` | **BodyLocation** | Anatomical location where the treatment should be applied (for example |

## `StructureDefinition-BeModelTask.json`

| Element | Glossary code | Model says |
|---|---|---|
| `author` | **Recorder** | Author of the task |
| `status` | **Status** | Status of the task |

## `StructureDefinition-BeModelTreatmentStatus.json`

| Element | Glossary code | Model says |
|---|---|---|
| `status` | **Status** | Status of the task |

## `StructureDefinition-BeModelVaccinationReduced.json`

| Element | Glossary code | Model says |
|---|---|---|
| `patient` | **Patient** | The patient that received vaccination. |
| `performer` | **Performer** | The professional that administered the medication |
| `administeredProduct.lotNumber` | **LotNumber** | The lot number |

## `StructureDefinition-PSSConsentModel.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date on which the information was recorded |

## `StructureDefinition-PSSRequest.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date on which the information was recorded |

## `StructureDefinition-PSSResponse.json`

| Element | Glossary code | Model says |
|---|---|---|
| `recordedDate` | **RecordedDate** | Date on which the information was recorded |
| `status` | **Status** | Status of the response |

## `StructureDefinition-be-model-allergyintolerance.json`

| Element | Glossary code | Model says |
|---|---|---|
| `reactions.note` | **Note** | Additional text note about the allergic reaction |

## `StructureDefinition-BeModelClinicalReport.json` - DRAFT

| Element | Glossary code | Model says |
|---|---|---|
| `businessIdentifier` | **BusinessIdentifier** | Business identifier of the report |
| `recordedDate` | **RecordedDate** | Date the report was recorded / last updated |
| `patient` | **Patient** | The patient the report is about |
| `recorder` | **Recorder** | Who recorded the report |
| `category` | **Category** | Clinical/functional classification of the report |
| `code` | **Code** | Code of the report |
| `note` | **Note** | Free-text additional information |
| `status` | **Status** | Status of the report |

## `StructureDefinition-BeModelDiagnosticReportDiabetes.json` - DRAFT

| Element | Glossary code | Model says |
|---|---|---|
| `BusinessIdentifier` | **BusinessIdentifier** | Report identifier for the internal supplier's business. |
| `RecordedDate` | **RecordedDate** | Date the report was produced. |
| `Patient` | **Patient** | We refer to the patient, subject of the report, by his unique identifi |
| `Recorder` | **Recorder** | This refers to the service provider or organization that encodes the i |
| `Performer` | **Performer** | We refer to the service provider or organization that collects the obs |
| `Category` | **Category** | Category of the report. According to ref. 8, it would be appropriate t |
| `Device` | **Device** | Identification number assigned by INAMI to the sensor type.See VS_Diab |
| `Code` | **Code** | Report code. In the diabetes project framework, it is proposed to indi |
| `Note` | **Note** | Report comments in free text format. This element will not be provided |
| `Status` | **Status** | Report status. By default it is “Final”. Value according to the busine |

## `StructureDefinition-BeModelObservationDiabetes.json` - DRAFT

| Element | Glossary code | Model says |
|---|---|---|
| `RecordedDate` | **RecordedDate** | Date of encoding of the observation by the Recorder. (DateTime format) |
| `Patient` | **Patient** | Is the unique identifier of the patient. The unique identifier must be |
| `Recorder` | **Recorder** |  Is the unique identifier (national register number)[1] of the health  |
| `Category` | **Category** | 698472009 “Glucose monitoring” (FR) (invariant)See VS_Obs_Dia_Category |
| `Status` | **Status** | 445665009 “Final report” - invariant. See VS_Obs_Diab_Status Status |
| `Code` | **Code** | Code corresponding to the derived value (coding to be established by S |

## `StructureDefinition-BeModeleBirthReport.json` - DRAFT

| Element | Glossary code | Model says |
|---|---|---|
| `businessIdentifier` | **BusinessIdentifier** | Business identifier for the eBirth report |
| `recordedDate` | **RecordedDate** | Date and time when the eBirth report was recorded or last update. |
| `patient` | **Patient** | The patient associated with the eBirth report. |
| `recorder` | **Recorder** | The practitioner who recorded the eBirth report. |
| `status` | **Status** | The status of the eBirth report, e.g., 'final', 'amended', 'cancelled' |
| `category` | **Category** | The category of the eBirth report. |
| `code` | **Code** | The code of the eBirth report. |
| `note` | **Note** | Notes or comments related to the eBirth report. |
