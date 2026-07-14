# Data card

## Data assets

The project uses a synthetic corpus, question bank, reference answers, evidence map, adversarial questions and refusal questions.

## Synthetic corpus

The corpus contains 10 Markdown documents covering organisational AI policy, data governance, security procedures, model monitoring, incident response, analytics platform use, evaluation procedures and privacy handling.

## Question bank

The question bank contains 60 records across factual, multi-hop, ambiguous, refusal and adversarial question types.

## Evidence map

Answerable questions are mapped to document sections with supporting evidence text and relevance labels. These rows support retrieval and citation evaluation.

## Reference answers

Reference answers are concise and limited to answerable questions. They are used as one support signal, not as the only quality measure.

## Adversarial and refusal questions

Unsupported and adversarial questions test refusal behaviour, evidence-only answering and human review routing.

## Limitations

Synthetic data is useful for public release and reproducibility, but it does not represent the scale or ambiguity of a live corpus.
