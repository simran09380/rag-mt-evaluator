export const mockEvaluation = {
  sentence_id: 1,

  source_language: "English",
  target_language: "Hindi",

  source_sentence:
    "The government announced a new policy today.",

  machine_translation:
    "सरकार ने आज एक नई नीति की घोषणा की।",

  reference:
    "सरकार ने एक नई नीति की घोषणा आज की।",

  overall_score: 93.4,

  quality_label: "Excellent",

  confidence: 0.91,

  dimension_scores: {
    accuracy: 96,
    fluency: 92,
    terminology: 95,
    named_entities: 100,
  },

  traditional_metrics: {
    BLEU: 0.82,
    METEOR: 0.89,
    chrF: 0.91,
    TER: 0.14,
    BERTScore: 0.94,
    COMET: 0.91,
  },

  retrieved_evidence: [
    {
      id: "E1",
      title: "Government Policy Document",
      content: "The government announced a new policy ...",
      relevance: 0.94,
      authority: 0.91,
      used_for: "Accuracy",
    },

    {
      id: "E2",
      title: "Official Terminology Database",
      content: "policy → नीति",
      relevance: 0.89,
      authority: 0.88,
      used_for: "Terminology",
    },

    {
      id: "E3",
      title: "Parallel Corpus",
      content: "सरकार ने नई नीति की घोषणा की ...",
      relevance: 0.82,
      authority: 0.85,
      used_for: "Fluency",
    },
  ],

  error_analysis: {
    total_errors: 7,
    major_errors: 2,
    minor_errors: 5,

    categories: [
      {
        name: "Mistranslation",
        count: 2,
      },
      {
        name: "Omission",
        count: 1,
      },
      {
        name: "Addition",
        count: 0,
      },
      {
        name: "Grammar",
        count: 2,
      },
      {
        name: "Word Order",
        count: 1,
      },
      {
        name: "Awkward",
        count: 1,
      },
      {
        name: "Wrong Terminology",
        count: 1,
      },
    ],
  },

  llm_evaluation: {
    accuracy: {
      score: 5,
      judgment:
        "The translation accurately preserves the meaning of the source sentence.",
      evidence_ids: ["E1"],
    },

    fluency: {
      score: 5,
      judgment:
        "The target-language output is completely natural, grammatical, and readable.",
      evidence_ids: [],
    },

    terminology: {
      score: 5,
      judgment:
        "Domain-specific terms are translated correctly and consistently.",
      evidence_ids: ["E2"],
    },

    named_entities: {
      score: 5,
      judgment:
        "All named entities are correctly translated and consistent.",
      evidence_ids: [],
    },
  },
};