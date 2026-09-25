export function mapEvaluationResponse(result) {
  const finalEvaluation = result?.final_evaluation || {};
  const metrics = result?.metrics || {};
  const referenceMetrics = metrics?.reference_based || {};
  const referenceFreeMetrics = metrics?.reference_free || {};
  const llmResponse = result?.llm_evaluation || {};
  const llm = llmResponse?.evaluation || {};
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

    confidence:
      finalEvaluation?.confidence ?? null,

    quality_label: getQualityLabel(
      finalEvaluation?.final_score
    ),

    traditional_metrics: {
      BLEU: referenceMetrics?.bleu ?? 0,

      chrF: referenceMetrics?.chrf ?? 0,

      "chrF++": referenceMetrics?.chrf_plus_plus ?? 0,

      METEOR: referenceMetrics?.meteor ?? 0,

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
      factual_consistency: scoreFromLLM(llm.factual_consistency),
      style: scoreFromLLM(llm.style),
      omissions: scoreFromLLM(llm.omissions),
      additions: scoreFromLLM(llm.additions),
    },

    llm_evaluation: {
      ...llm,
      model: llmResponse?.model || null,
      supported_by_evidence:
        llmResponse?.supported_by_evidence ?? false,
    },

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

  const allEvidence = [];

  Object.entries(retrieval).forEach(
    ([queryType, queryData]) => {
      const results = queryData?.results;

      if (!Array.isArray(results)) {
        return;
      }

      results.forEach((item) => {
        allEvidence.push({
          id: `temp-${allEvidence.length}`,

          title:
            item?.metadata?.source_type ||
            item?.chunk_type ||
            "Retrieved Evidence",

          content:
            item?.text ||
            item?.target ||
            item?.target_text ||
            item?.source ||
            "",

          relevance: Number(item?.relevance ?? 0),

          authority: Number(
            item?.authority_score ?? 0
          ),

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

          semantic_score: Number(
            item?.semantic_score ?? 0
          ),

          source_similarity: Number(
            item?.source_similarity ?? 0
          ),

          hypothesis_similarity: Number(
            item?.hypothesis_similarity ?? 0
          ),

          terminology_score: Number(
            item?.terminology_score ?? 0
          ),

          entity_score: Number(
            item?.entity_score ?? 0
          ),

          verification_score: Number(
            item?.verification_score ?? 0
          ),
        });
      });
    }
  );

  // Remove duplicate evidence
  const uniqueEvidence = Array.from(
    new Map(
      allEvidence.map((item) => [
        `${item.title}-${item.content}`,
        item,
      ])
    ).values()
  );

  // Highest relevance first
  uniqueEvidence.sort(
    (a, b) => b.relevance - a.relevance
  );

  // Show only top 3 in UI
  return uniqueEvidence
    .slice(0, 3)
    .map((item, index) => ({
      ...item,
      id: `E${index + 1}`,
    }));
}

export function mapDatasetResults(datasetResult) {
  const records = Array.isArray(datasetResult?.data)
    ? datasetResult.data
    : [];

  return records.map((record) => {
    const finalScore =
      record?.final_evaluation?.final_score ?? 0;

    return {
      sentence_id: record?.id,
      source: record?.source || "",
      translation: record?.hypothesis || "",
      reference: record?.reference || "",
      overall_score: finalScore,
      quality_label: getQualityLabel(finalScore),
      error_count:
        record?.mqm_evaluation?.total_errors ?? 0,

      // Keep the original backend record.
      // We need this when the user clicks the row.
      rawRecord: record,
    };
  });
}


export function mapDatasetRecordToEvaluation(
  record,
  datasetResult
) {
  if (!record) return null;

  const metrics = record?.metrics || {};
  const referenceMetrics =
    metrics?.reference_based || {};
  const referenceFreeMetrics =
    metrics?.reference_free || {};

  const llm =
    record?.llm_evaluation?.evaluation || {};

  const mqm =
    record?.mqm_evaluation || {};

  const finalEvaluation =
    record?.final_evaluation || {};

  /*
   * Find retrieval belonging ONLY to this sentence.
   */
  const recordRetrieval = Array.isArray(
    datasetResult?.query_retrieval
  )
    ? datasetResult.query_retrieval.find(
        (item) =>
          String(item?.record_id) ===
          String(record?.id)
      )
    : null;

  return {
    sentence_id: record?.id,

    source_language:
      record?.source_lang ||
      record?.preprocessing?.source_language ||
      "en",

    target_language:
      record?.target_lang ||
      record?.preprocessing?.target_language ||
      "hi",

    source_sentence:
      record?.source || "",

    machine_translation:
      record?.hypothesis || "",

    reference:
      record?.reference || "",

    overall_score:
      finalEvaluation?.final_score ?? 0,

    quality_label: getQualityLabel(
      finalEvaluation?.final_score
    ),

    confidence:
      finalEvaluation?.confidence ?? null,

    traditional_metrics: {
      BLEU:
        referenceMetrics?.bleu ?? 0,

      METEOR:
        referenceMetrics?.meteor ?? 0,

      chrF:
        referenceMetrics?.chrf ?? 0,

      "chrF++":
        referenceMetrics?.chrf_plus_plus ?? 0,

      TER:
        referenceMetrics?.ter ?? 0,

      BERTScore:
        referenceMetrics?.bertscore ?? 0,

      COMET:
        referenceMetrics?.comet ?? 0,
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
      factual_consistency:
        scoreFromLLM(llm.factual_consistency),
      style: scoreFromLLM(llm.style),
      omissions: scoreFromLLM(llm.omissions),
      additions: scoreFromLLM(llm.additions),
    },

    llm_evaluation: {
      ...llm,

      model:
        record?.llm_evaluation?.model || null,

      supported_by_evidence:
        record?.llm_evaluation
          ?.supported_by_evidence ?? false,
    },

    mqm_evaluation: mqm,

    error_analysis:
      mapMQMToErrorAnalysis(mqm),

    retrieved_evidence:
      mapRetrievalToEvidence(
        recordRetrieval?.retrieval
      ),

    final_evaluation: finalEvaluation,
  };
}