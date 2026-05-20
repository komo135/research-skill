# Landmark Examples

Use these as calibration examples for proposition content, not as templates to imitate.

## ResNet-Style Move

- Surprise: deeper plain networks can have worse training error.
- Bit: adding depth should not make optimization worse because identity-like layers should be available.
- Flip: expose identity-neighborhood solutions through residual parameterization.
- Discriminating exam: compare plain versus residual parameterization under matched depth and data.
- Lesson: the contribution is not "use skip connections"; it is a load-bearing Bit plus a tractable Flip.

## Transformer/GPT-Style Move

- Surprise: sequence modeling quality and scalability are bottlenecked by recurrence and task-specific supervision.
- Bit: long-context language behavior requires specialized sequential machinery and task-specific labels.
- Flip: move the learning problem into broad next-token prediction with scalable attention.
- Discriminating exam: scaling and transfer behavior separate the proposition from narrower supervised or recurrent explanations.
- Lesson: landmark ambition needs a field-level Bit and a discriminator, not grand wording.

## Honest Incremental Move

- Surprise: a method improves only on a narrow slice.
- Bit: the slice exposes a real but local assumption.
- Flip: state the proposition narrowly and mark `Ambition: incremental-honest`.
- Discriminating exam: show the slice, the comparator, and the limitation without implying a field-wide result.
