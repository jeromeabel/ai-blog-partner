# Blogger Partner Architecture

Variables:
- blog_id
- step_id

## Step 1: draft to outlines
- input: Read and analyse DRAFT content of the blog post in "inputs/<blog_id>" folder
- Create outlines following Blog Style and Constraint ("inputs/instructions.md"), human in the loop / iteration brainstorming (choose best interaction mode, must be partner style, stimulating for me as human), step by step, just the headings and a short sentence if necessary for sections: Title, Subtitle, Introduction, Body, Conclusion
- Check Human Validation 
- TOOLS_file. Create the validated "outputs/<blog_id>/<step_id>_outlines.md" file
- TOOLS_file. Split the DRAFT into two files: "outputs/<blog_id>/<step_id>_draft_ok.md" and "outputs/<blog_id>/<step_id>_draft_not_ok.md". The LLM MUST NOT write text just COPY original text to one of this two file, according to the validated outlines, which act as a filter. the 'not_ok' file will be used as material for next blog posts.
- TOOLS_script: Check if content of this two files are valid: all the first draft must be inside the two files, the two files are a partition, with no overlap.
- Success, Error

## Step 2 (automatic) : outlines to draft organized
- inputs: outlines.md + draft_ok.md
- Create a "outputs/<blog_id>/<step_id>_draft_organized.md" file that is a reorganized version of the draft_ok.md file, following the outlines.md file. The LLM MUST NOT write text just COPY original text and move pieces of text according to the outlines.
- Check : success, error

## Step 3: outlines to sections step by step
- input: outlines.md + draft_organized.md
- loop through each section of the outline to create 80-100% perfect text content following style guidelines/constraints (next will be finalized after): iterative/partner mode. RULE. Check Data sources, gooogle search to check or add relevant information. + English Coach (triggered everytime I write, but advices should appear only manually with human interaction or if english mistakes are enough useful for me). REFERENCE LINKS should be a footnotes. English coach will memorize long-term in a specific file mistakes. To provide a nice summary at the end of the section. English coach annotations should not break the flow or writing. IMPORTANT: sometimes the outlines.md might change in the creative/writing process. IMPORTANT: too much changes is hard to follow, as a human do change/modify in a natural way to stimulate writing processs.
  - If human validation, go to next section, and write final version of the section in "outputs/<blog_id>/<step_id>_draft_nice.md"
- if all the content are passed through a score of > 80%, go to next section

## Step 4: draft_nice to draft_polished
- input: outlines.md + draft_nice.md
- same loop to refine/polish each sections
  - If human validation, go to next section, and write final version of the section in "outputs/<blog_id>/<step_id>_draft_polished.md"

## Step 5: draft_polished to final
- input: draft_polished.md
- add SEO meta description
- respect the final markdown format of my blog post
- create the last final version in "outputs/<blog_id>/<step_id>_final.md"

## Step 6 (optional): illustration cover
- iterative brainstorming of different ideas for an illustration cover (art instructions is missing, and depends of the blog post or the series)
- if LLM is capable, generate an illustration cover or some part to help me compose and make it myself
