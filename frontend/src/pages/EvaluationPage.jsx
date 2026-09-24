import { useState } from "react";
import { mapEvaluationResponse } from "../utils/evaluationMapper";

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

import { mockDataset } from "../data/mockDataset";


import { evaluateTranslation } from "../api/evaluationApi";

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
  setEvaluationResult(null);
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

      console.log("RESULT TYPE:", typeof result);
      console.log("RESULT:", result);
      console.log("RESULT JSON:", JSON.stringify(result, null, 2));

      const mappedResult = mapEvaluationResponse(result);

      console.log("MAPPED FRONTEND RESULT:", mappedResult);

      setEvaluationResult(mappedResult);

      setIsEvaluating(false);
      setShowResults(true);

    } catch (error) {
      console.error("Evaluation API Error:", error);

      setIsEvaluating(false);
    }

    return;
  }

  // Dataset flow remains unchanged for now
  let step = 1;

  const interval = setInterval(() => {
    step += 1;

    setCurrentStep(step);

    if (step === 10) {
      clearInterval(interval);

      setTimeout(() => {
        setIsEvaluating(false);
        setShowResults(true);
      }, 800);
    }
  }, 700);
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
            />

          </div>


          {/* Second Result Row */}
          <div className="mt-6 grid gap-6 xl:grid-cols-3">

            <TraditionalMetrics
              metrics={evaluationResult.traditional_metrics}
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
          />

        </div>
      )}


      {showResults && evaluationMode === "dataset" && (
        <div className="animate-[fadeIn_0.5s_ease-out]">

          <DatasetSummary
            dataset={mockDataset}
          />

          <SentenceResultsTable
            results={mockDataset.results}
            onSelectSentence={(sentence) => {
              setSelectedDatasetSentence(sentence);
            }}
          />

          {selectedDatasetSentence && (
        <div className="mt-8 animate-[fadeIn_0.5s_ease-out]">

          {/* Selected Sentence Header */}
          <div className="mb-6 flex items-center justify-between">

            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-violet-400">
                Detailed Evaluation
              </p>

              <h2 className="mt-1 text-2xl font-bold">
                Sentence #{selectedDatasetSentence.sentence_id}
              </h2>

              <p className="mt-2 text-xs text-slate-500">
                Complete evaluation results for the selected sentence.
              </p>
            </div>

            <button
              onClick={() => setSelectedDatasetSentence(null)}
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


          {/* Detailed Evaluation */}
          <div className="grid gap-6 xl:grid-cols-3">

            <OverallEvaluation
              evaluation={{
                ...evaluationResult,
                sentence_id: selectedDatasetSentence.sentence_id,
                source_sentence: selectedDatasetSentence.source,
                machine_translation: selectedDatasetSentence.translation,
                overall_score: selectedDatasetSentence.overall_score,
                quality_label: selectedDatasetSentence.quality_label,
              }}
            />

            <TranslationComparison
              evaluation={{
                ...evaluationResult,
                sentence_id: selectedDatasetSentence.sentence_id,
                source_sentence: selectedDatasetSentence.source,
                machine_translation: selectedDatasetSentence.translation,
                overall_score: selectedDatasetSentence.overall_score,
                quality_label: selectedDatasetSentence.quality_label,
              }}
            />

            <DimensionScores
              scores={evaluationResult.dimension_scores}
            />

          </div>


          <div className="mt-6 grid gap-6 xl:grid-cols-3">

            <TraditionalMetrics
              metrics={evaluationResult.traditional_metrics}
            />

            <RetrievedEvidence
              evidence={evaluationResult.retrieved_evidence}
            />

            <ErrorAnalysis
              errorAnalysis={evaluationResult.error_analysis}
            />

          </div>


          <LLMEvaluation
            evaluation={evaluationResult.llm_evaluation}
          />

        </div>
      )}

        </div>
      )}

      </main>

    </div>
  );
}

export default EvaluationPage;