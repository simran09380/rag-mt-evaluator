import { useState } from "react";
import {
  mapEvaluationResponse,
  mapDatasetResults,
  mapDatasetRecordToEvaluation,
} from "../utils/evaluationMapper";


import Navbar from "../components/Navbar";
import EvaluationInput from "../components/EvaluationInput";
import EvaluationPipeline from "../components/EvaluationPipeline";

import OverallEvaluation from "../components/OverallEvaluation";
import TranslationComparison from "../components/TranslationComparison";
import DimensionScores from "../components/DimensionScores";

import TraditionalMetrics from "../components/TraditionalMetrics";
import RetrievedEvidence from "../components/RetrievedEvidence";
import ErrorAnalysis from "../components/ErrorAnalysis";

import LLMEvaluation from "../components/LLMEvaluation";

import DatasetSummary from "../components/DatasetSummary";
import SentenceResultsTable from "../components/SentenceResultsTable";

import { evaluateTranslation,evaluateDataset, } from "../api/evaluationApi";

function EvaluationPage() {
  const [selectedDatasetSentence, setSelectedDatasetSentence] = useState(null);
  const [evaluationMode, setEvaluationMode] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);

  const handleEvaluate = async (inputData) => {
  console.log("Evaluation Input:", inputData);

  setEvaluationMode(inputData.mode);
  setSelectedDatasetSentence(null);
  setShowResults(false);
  setIsEvaluating(true);
  setCurrentStep(1);

  if (inputData.mode === "sentence") {
    try {
      const result = await evaluateTranslation({
        source: inputData.source,
        hypothesis: inputData.translation,
        reference: inputData.reference,
        sourceLang: "en",
        targetLang: "hi",
        domain: inputData.domain,
      });

      const mappedResult =
        mapEvaluationResponse(result);

      setEvaluationResult(mappedResult);

      setIsEvaluating(false);
      setCurrentStep(10);
      setShowResults(true);
    } catch (error) {
      console.error(
        "Evaluation API Error:",
        error
      );

      setIsEvaluating(false);
      setShowResults(false);
    }

    return;
  }

  if (inputData.mode === "dataset") {
    try {
      const result = await evaluateDataset({
        file: inputData.file,
        sourceLang: "en",
        targetLang: "hi",
        domain: inputData.domain || "General",
      });

      console.log(
        "DATASET RESULT:",
        result
      );

      setEvaluationResult(result);

      setIsEvaluating(false);
      setCurrentStep(10);
      setShowResults(true);
    } catch (error) {
      console.error(
        "Dataset Evaluation API Error:",
        error
      );

      setIsEvaluating(false);
      setShowResults(false);
    }

    return;
  }
};

  return (
    <div className="min-h-screen bg-[#050816] text-white">

      <Navbar />

      <main className="mx-auto max-w-[1500px] px-6 py-8">

        {/* Page Header */}
        <section className="mb-8">

          <p className="mb-2 text-sm font-medium uppercase tracking-wider text-violet-400">
            Translation Evaluation Workbench
          </p>

          <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
            Evaluate your machine translation
          </h1>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
            Analyze translation quality using traditional metrics,
            retrieval evidence, evidence-grounded LLM evaluation,
            and MQM error classification.
          </p>

        </section>


        {/* Input */}
        <EvaluationInput
          onEvaluate={handleEvaluate}
        />


        {/* Pipeline */}
        <EvaluationPipeline
          currentStep={currentStep}
          isEvaluating={isEvaluating}
        />


        {/* Results */}
        {showResults && evaluationMode === "sentence" && (
        <div className="animate-[fadeIn_0.5s_ease-out]">

          {/* First Result Row */}
          <div className="mt-6 grid gap-6 xl:grid-cols-3">

            <OverallEvaluation
              evaluation={evaluationResult}
            />

            <TranslationComparison
              evaluation={evaluationResult}
            />

            <DimensionScores
              scores={evaluationResult.dimension_scores}
              llmEvaluation={evaluationResult.llm_evaluation}
            />

          </div>


          {/* Second Result Row */}
          <div className="mt-6 grid gap-6 xl:grid-cols-3">

            <TraditionalMetrics
              metrics={evaluationResult.traditional_metrics}
              referenceFreeMetrics={evaluationResult.reference_free_metrics}
            />

            <RetrievedEvidence
              evidence={evaluationResult.retrieved_evidence}
            />

            <ErrorAnalysis
              errorAnalysis={evaluationResult.error_analysis}
            />

          </div>


          {/* LLM Evaluation */}
          <LLMEvaluation
            evaluation={evaluationResult.llm_evaluation}
            evidence={evaluationResult.retrieved_evidence}
          />

        </div>
      )}


      {showResults && evaluationMode === "dataset" && (
  <div className="animate-[fadeIn_0.5s_ease-out]">

    {/* Dataset Summary */}
    <DatasetSummary
      dataset={evaluationResult}
    />

    {/* Sentence Results */}
    <SentenceResultsTable
      results={mapDatasetResults(
        evaluationResult
      )}
      onSelectSentence={(sentence) => {
        setSelectedDatasetSentence(
          sentence
        );
      }}
    />

    {/* Selected Sentence */}
    {selectedDatasetSentence && (
      <DatasetSentenceDetails
        sentence={selectedDatasetSentence}
        datasetResult={evaluationResult}
        onClose={() =>
          setSelectedDatasetSentence(null)
        }
      />
    )}

  </div>
)}

      </main>

    </div>
  );
}

function DatasetSentenceDetails({
  sentence,
  datasetResult,
  onClose,
}) {
  const evaluation =
    mapDatasetRecordToEvaluation(
      sentence?.rawRecord,
      datasetResult
    );

  if (!evaluation) {
    return null;
  }

  return (
    <div className="mt-8 animate-[fadeIn_0.5s_ease-out]">

      {/* Header */}
      <div className="mb-6 flex items-center justify-between">

        <div>

          <p className="text-xs font-medium uppercase tracking-wider text-violet-400">
            Detailed Evaluation
          </p>

          <h2 className="mt-1 text-2xl font-bold text-white">
            Sentence #{sentence.sentence_id}
          </h2>

          <p className="mt-2 text-xs text-slate-500">
            Complete evaluation results for the selected sentence.
          </p>

        </div>

        <button
          onClick={onClose}
          className="
            rounded-xl
            border border-white/10
            bg-white/[0.03]
            px-4 py-2
            text-xs
            text-slate-400
            transition
            hover:bg-white/[0.06]
            hover:text-white
          "
        >
          Close Details
        </button>

      </div>


      {/* Row 1 */}
      <div className="grid gap-6 xl:grid-cols-3">

        <OverallEvaluation
          evaluation={evaluation}
        />

        <TranslationComparison
          evaluation={evaluation}
        />

        <DimensionScores
          scores={evaluation.dimension_scores}
          llmEvaluation={
            evaluation.llm_evaluation
          }
        />

      </div>


      {/* Row 2 */}
      <div className="mt-6 grid gap-6 xl:grid-cols-3">

        <TraditionalMetrics
          metrics={
            evaluation.traditional_metrics
          }
          referenceFreeMetrics={
            evaluation.reference_free_metrics
          }
        />

        <RetrievedEvidence
          evidence={
            evaluation.retrieved_evidence
          }
        />

        <ErrorAnalysis
          errorAnalysis={
            evaluation.error_analysis
          }
        />

      </div>


      {/* LLM Evaluation */}
      <LLMEvaluation
        evaluation={
          evaluation.llm_evaluation
        }
        evidence={
          evaluation.retrieved_evidence
        }
      />

    </div>
  );
}

export default EvaluationPage;