export function mapEvaluationResponse(result) {
  const finalEvaluation = result?.final_evaluation || {};
  const metrics = result?.metrics || {};
  const referenceMetrics = metrics?.reference_based || {};
  const referenceFreeMetrics = metrics?.reference_free || {};
  const llm = result?.llm_evaluation?.evaluation || {};
  const mqm = result?.mqm_evaluation || {};

  return {
    sentence_id: 1,

    source_language:
      result?.preprocessing?.source_language || "en",

    target_language:
      result?.preprocessing?.target_language || "hi",

    source_sentence: result?.source || "",

    machine_translation: result?.hypothesis || "",

    reference: result?.reference || "",

    overall_score:
      finalEvaluation?.final_score ?? 0,

    quality_label: getQualityLabel(
      finalEvaluation?.final_score
    ),

    traditional_metrics: {
      BLEU: referenceMetrics?.bleu ?? 0,
      METEOR: referenceMetrics?.meteor ?? 0,
      chrF: referenceMetrics?.chrf ?? 0,
      TER: referenceMetrics?.ter ?? 0,
      BERTScore: referenceMetrics?.bertscore ?? 0,
      COMET: referenceMetrics?.comet ?? 0,
    },

    reference_free_metrics: {
      multilingual_similarity:
        referenceFreeMetrics?.multilingual_similarity ?? 0,

      word_alignment_coverage:
        referenceFreeMetrics?.word_alignment_coverage ?? 0,

      entity_preservation:
        referenceFreeMetrics?.entity_preservation ?? 0,

      terminology_accuracy:
        referenceFreeMetrics?.terminology_accuracy ?? 0,

      length_ratio:
        referenceFreeMetrics?.length_ratio ?? 0,

      untranslated_token_ratio:
        referenceFreeMetrics?.untranslated_token_ratio ?? 0,
    },

    dimension_scores: {
      accuracy: scoreFromLLM(llm.accuracy),
      fluency: scoreFromLLM(llm.fluency),
      terminology: scoreFromLLM(llm.terminology),
      named_entities: scoreFromLLM(llm.named_entities),
    },

    llm_evaluation: llm,

    mqm_evaluation: mqm,

    error_analysis: mapMQMToErrorAnalysis(mqm),

    retrieved_evidence: mapRetrievalToEvidence(
      result?.retrieval
    ),

    final_evaluation: finalEvaluation,
  };
}


function scoreFromLLM(dimension) {
  if (!dimension || typeof dimension.score !== "number") {
    return 0;
  }

  return dimension.score * 20;
}


function getQualityLabel(score) {
  if (typeof score !== "number") {
    return "Not Available";
  }

  if (score >= 90) {
    return "Excellent";
  }

  if (score >= 75) {
    return "Good";
  }

  if (score >= 60) {
    return "Needs Review";
  }

  return "Poor";
}


function mapMQMToErrorAnalysis(mqm) {
  const errors = Array.isArray(mqm?.errors)
    ? mqm.errors
    : [];

  return {
    total_errors: mqm?.total_errors ?? errors.length,
    total_penalty: mqm?.total_penalty ?? 0,
    major_errors: errors.filter(
      (error) =>
        String(error?.severity || "").toLowerCase() === "major"
    ).length,
    minor_errors: errors.filter(
      (error) =>
        String(error?.severity || "").toLowerCase() === "minor"
    ).length,
    categories: [],
    errors,
  };
}


function mapRetrievalToEvidence(retrieval) {
  if (!retrieval || typeof retrieval !== "object") {
    return [];
  }

  const evidence = [];

  Object.entries(retrieval).forEach(
    ([queryType, queryData]) => {
      const results = queryData?.results;

      if (!Array.isArray(results)) {
        return;
      }

      results.forEach((item, index) => {
        evidence.push({
          id: `E${evidence.length + 1}`,

          title:
            item?.metadata?.source_type ||
            item?.chunk_type ||
            queryType,

          content:
            item?.target ||
            item?.target_text ||
            item?.text ||
            item?.source ||
            "",

          relevance: item?.relevance ?? 0,

          authority:
            item?.authority_score ??
            0,

          used_for: queryType,

          query_type: queryType,

          chunk_type:
            item?.chunk_type ||
            item?.metadata?.chunk_type ||
            "",

          source: item?.source || "",

          target:
            item?.target ||
            item?.target_text ||
            "",

          semantic_score:
            item?.semantic_score ?? 0,

          source_similarity:
            item?.source_similarity ?? 0,

          hypothesis_similarity:
            item?.hypothesis_similarity ?? 0,

          terminology_score:
            item?.terminology_score ?? 0,

          entity_score:
            item?.entity_score ?? 0,

          verification_score:
            item?.verification_score ?? 0,
        });
      });
    }
  );

  return evidence;
}