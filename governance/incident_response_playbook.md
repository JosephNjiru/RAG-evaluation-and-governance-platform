# Incident response playbook

## Unsupported answer incident

1. Identify the question ID and answer record.
2. Check cited evidence and evidence map rows.
3. Mark the answer as unsupported.
4. Add the record to human review.
5. Update retrieval, refusal or corpus controls as needed.

## Wrong citation incident

1. Record the wrong citation label.
2. Compare the citation with expected evidence rows.
3. Correct citation formatting or retrieval behaviour.
4. Re-run citation metrics.

## Unsafe response incident

1. Preserve the question and answer record.
2. Mark the safety flag.
3. Stop using the output for any decision.
4. Review the safety rule and refusal behaviour.

## Sensitive information exposure

1. Remove the exposed material from public artefacts.
2. Check corpus source files and generated outputs.
3. Rotate any affected secret if a real secret was exposed.
4. Add a prevention check to the quality scan where possible.

## Evaluation score misuse

1. Identify the unsupported claim.
2. Correct README, reports or portfolio material.
3. Confirm limitations are visible.
4. Re-run quality scan.

## Corpus update error

1. Identify changed corpus files.
2. Rebuild chunks and vector index.
3. Re-run RAG answers and evaluation.
4. Check evidence map coverage and report changes.
