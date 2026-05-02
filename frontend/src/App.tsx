import React, { useState } from 'react';
import { Tabs, TabList, Tab, TabPanels, TabPanel } from '@carbon/react';
import DashboardHeader from './sections/DashboardHeader';
import InputSection from './sections/InputSection';
import DiagnoseSection from './sections/DiagnoseSection';
import PrescribeSection from './sections/PrescribeSection';
import TreatSection from './sections/TreatSection';
import { AnalyzeResponse, FixResponse, PRResponse } from './services/api';

export type Phase = 'input' | 'diagnose' | 'prescribe' | 'treat';

const PHASE_INDEX: Record<Phase, number> = {
  input: 0,
  diagnose: 1,
  prescribe: 2,
  treat: 3,
};

/**
 * ProcessDoctor — Single Dashboard Architecture
 *
 * Why one dashboard instead of five screens:
 *   - Faster to build in a 24-hour hackathon
 *   - Less navigation logic = less to break during the live demo
 *   - The phase tabs provide the diagnose -> prescribe -> treat narrative
 *     without requiring router-based screen transitions
 *
 * The user clicks through phase tabs as they progress. The active phase
 * scrolls into view, and previous phases stay accessible for reference
 * during the demo.
 */
const App: React.FC = () => {
  const [phase, setPhase] = useState<Phase>('input');
  const [inputValue, setInputValue] = useState('');
  const [inputType, setInputType] = useState<'text' | 'github'>('text');
  const [hasAnalyzed, setHasAnalyzed] = useState(false);
  
  // API response state
  const [analysisData, setAnalysisData] = useState<AnalyzeResponse | null>(null);
  const [fixData, setFixData] = useState<FixResponse | null>(null);
  const [prData, setPRData] = useState<PRResponse | null>(null);

  const handleDiagnose = (text: string, type: 'text' | 'github') => {
    setInputValue(text);
    setInputType(type);
    setHasAnalyzed(true);
    setPhase('diagnose');
  };

  const handleAnalysisComplete = (data: AnalyzeResponse) => {
    setAnalysisData(data);
  };

  const handleFixComplete = (data: FixResponse) => {
    setFixData(data);
  };

  const handlePRComplete = (data: PRResponse) => {
    setPRData(data);
  };

  return (
    <>
      {/* Skip link for keyboard users (WCAG 2.4.1) */}
      <a href="#main" className="pd-skip-link">Skip to main content</a>

      <main id="main" role="main">
        <DashboardHeader />

        <div className="pd-container" style={{ paddingBottom: 'var(--pd-space-12)' }}>
          {/* Phase tabs - the diagnose -> prescribe -> treat indicator */}
          <Tabs
            selectedIndex={PHASE_INDEX[phase]}
            onChange={({ selectedIndex }) => {
              const phases: Phase[] = ['input', 'diagnose', 'prescribe', 'treat'];
              const target = phases[selectedIndex];
              // Don't allow jumping ahead before analysis runs
              if (!hasAnalyzed && PHASE_INDEX[target] > 0) return;
              setPhase(target);
            }}
          >
            <TabList aria-label="Workflow phases" contained>
              <Tab>1. Input</Tab>
              <Tab disabled={!hasAnalyzed}>2. Diagnose</Tab>
              <Tab disabled={!hasAnalyzed}>3. Prescribe</Tab>
              <Tab disabled={!hasAnalyzed}>4. Treat</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <InputSection
                  onDiagnose={handleDiagnose}
                />
              </TabPanel>
              <TabPanel>
                <DiagnoseSection
                  inputDescription={inputValue}
                  inputType={inputType}
                  onContinue={() => setPhase('prescribe')}
                  onAnalysisComplete={handleAnalysisComplete}
                  analysisData={analysisData}
                />
              </TabPanel>
              <TabPanel>
                <PrescribeSection
                  onApprove={() => setPhase('treat')}
                  analysisData={analysisData}
                  onFixComplete={handleFixComplete}
                  fixData={fixData}
                />
              </TabPanel>
              <TabPanel>
                <TreatSection
                  fixData={fixData}
                  onPRComplete={handlePRComplete}
                  prData={prData}
                  onRestart={() => {
                    setPhase('input');
                    setHasAnalyzed(false);
                    setInputValue('');
                    setAnalysisData(null);
                    setFixData(null);
                    setPRData(null);
                  }}
                />
              </TabPanel>
            </TabPanels>
          </Tabs>
        </div>
      </main>
    </>
  );
};

export default App;
