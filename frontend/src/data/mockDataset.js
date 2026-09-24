export const mockDataset = {
  total_sentences: 5,
  evaluated_sentences: 5,
  average_score: 88.6,

  quality_distribution: {
    excellent: 2,
    good: 2,
    needs_review: 1,
  },

  results: [
    {
      sentence_id: 1,
      source:
        "The government announced a new policy today.",
      translation:
        "सरकार ने आज एक नई नीति की घोषणा की।",
      overall_score: 93.4,
      quality_label: "Excellent",
      error_count: 0,
    },

    {
      sentence_id: 2,
      source:
        "The new policy will improve public services.",
      translation:
        "नई नीति सार्वजनिक सेवाओं में सुधार करेगी।",
      overall_score: 91.2,
      quality_label: "Excellent",
      error_count: 1,
    },

    {
      sentence_id: 3,
      source:
        "The ministry released the report yesterday.",
      translation:
        "मंत्रालय ने रिपोर्ट कल जारी की।",
      overall_score: 86.7,
      quality_label: "Good",
      error_count: 1,
    },

    {
      sentence_id: 4,
      source:
        "The program will provide financial support.",
      translation:
        "कार्यक्रम वित्तीय सहायता प्रदान करेगा।",
      overall_score: 79.5,
      quality_label: "Good",
      error_count: 2,
    },

    {
      sentence_id: 5,
      source:
        "The committee rejected the proposal.",
      translation:
        "समिति ने प्रस्ताव को स्वीकार किया।",
      overall_score: 62.4,
      quality_label: "Needs Review",
      error_count: 3,
    },
  ],
};