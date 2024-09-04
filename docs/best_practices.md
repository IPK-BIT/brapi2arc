# Best Practices
You will find here a list of all requirements and assumptions, that need to be fulfilled so that you can use your ARC with brapi2arc.

## Assumptions made
- Each study has one assay that has the same identifier. This is necessary as BrAPI does not know the concept of assays and we need a way to know in which assay the observations should be written to.
- The assay already exists and might not yet have a Phenotyping sheet in it. This is necessary so that the assay is at no point empty and the basic information is already set.

## Required information
- If you want to set the study design through brapi2arc, you can leave the output and factor columns of the study empty, but you need to already add each material to the study. This is necessary so that the germplasm information is available and can be used to check if the study includes the material.
- Each observation unit needs to have a GRID ROW and a GRID COLUMN as a study factor. This is necessary as the location in the grid and the germplasm name is used as identifier of the observation unit.