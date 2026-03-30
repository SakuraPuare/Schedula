/**
 * Feature F23 - Student course selection orchestrator.
 * Design intent: switch between plan browsing and class-level selection details while
 * preserving the selected course context.
 */
import React, { useState } from 'react';
import CourseContentPlan from './plan';
import CourseContentClasser from './classer';
const CourseContent = () => {
  const [mode, setMode] = useState('plan');
  const [planID, setPlanID] = useState(0);
  const [page, setPage] = useState(1);

  return (
    <>
      {mode === 'plan' ? (
        <CourseContentPlan setMode={setMode} setPlanID={setPlanID} setPage={setPage} page={page}/>
      ) : (
        < CourseContentClasser setMode={setMode} classplanid={planID}/>
      )}
    </>
  );
};

export default CourseContent;
