# Action Plan for Frontend Refactoring Cleanup

## Issue Description
The project recently underwent a refactoring to limit the use of Astro templates. This process was challenging and resulted in leftover unused code. This action plan addresses the need to clean up the interaction between Server-Side Rendering (SSR) and Client-Side Rendering (CSR) components, as well as interactions with the backend API.

## Relevant Codebase Parts
1.  **`frontend/src/pages/`**: Contains Astro pages, central to SSR. The refactor aimed to limit their use.
2.  **`frontend/src/components/`**: Houses React components (CSR) and potentially some Astro components. Key for CSR interactions.
3.  **`frontend/src/layouts/`**: Astro layouts used by pages, part of the SSR structure that was refactored.
4.  **`frontend/src/lib/`**: Likely contains frontend API client logic and utilities, relevant to backend API interaction cleanup.
5.  **`backend/app/api/`**: Backend API endpoint definitions. May have unused endpoints due to frontend changes.
6.  **`frontend/src/types.ts`**: Shared type definitions that might be outdated after refactoring.

## Git Commit History Analysis
- A significant refactoring effort occurred around mid-May 2025, notably with commits like "Limit the use of Astro" (commit `caa4c09296f9a2dbe6314a769b96ee96bf14eabc`) and "Refactor: consolidate layouts into single BaseLayout" (commit `fd0efac756d8992a3f30699c8c616fb01caf9b3a`).
- This refactoring was followed by several fixes related to refresh problems (e.g., commit `ca19adcc2b9d8f275a3d92a3b89df92793b59085` impacting pages, components, and lib) and linter errors in `frontend/src/components/`.
- These subsequent fixes suggest the initial refactoring may have been complex, potentially leaving behind unused code or creating new integration challenges between SSR and CSR.
- All relevant recent commits were authored by Marysia Lowas-Rzechonek.

## Root Cause Hypothesis
The most likely root cause is a combination of **incomplete refactoring** and resultant **dead code**. The explicit goal to "Limit the use of Astro" implies a shift in architecture. The issue description's statement that "refactoring has hard and left a lot of unused code" strongly supports this. The subsequent fixes for refresh issues and linting problems indicate that the transition to a more client-side React-heavy approach might not have been entirely smooth, leaving behind unused Astro artifacts and potentially awkward or inefficient SSR/CSR and API integrations.

## Potential Contacts
1.  **Marysia Lowas-Rzechonek**:
    *   *Reasoning*: As the primary author of the recent refactoring commits (including "Limit the use of Astro") and other subsequent fixes, she possesses the most in-depth knowledge of the changes, the intended architecture, and any known issues.

## Investigation Questions
1.  Which specific Astro files in `frontend/src/pages/` and `frontend/src/layouts/` are still actively used and rendering significant unique content, versus those that could be further simplified or replaced by client-side rendering?
2.  What is the current, intended pattern for data fetching and passing data from Astro (SSR) to React components (CSR)? Are there areas where this is inconsistent or could be streamlined?
3.  Are there any `.astro` components remaining in `frontend/src/components/` that are now redundant or could be more effectively implemented as React components?
4.  How do the current Astro layouts and React component-based layouts divide responsibilities? Is there any functional overlap or redundancy to address?
5.  Which specific API client functions within `frontend/src/lib/` are actively invoked by the current frontend (pages and components)?
6.  Conversely, are there any API endpoints in `backend/app/api/` that might now be orphaned (no longer called by the frontend) as a result of the refactoring?
7.  How is page hydration currently managed? Are there specific scenarios (like the "refresh problem" mentioned in commits) that highlight issues in the SSR/CSR state reconciliation?
8.  (For Marysia) What were the primary drivers and goals behind the "Limit the use of Astro" initiative? This will help ensure the cleanup aligns with those goals.
9.  (For Marysia) Were there any specific areas of known technical debt or "pain points" concerning SSR/CSR interaction or API usage that were identified during or after the refactoring?
10. (For Marysia) What is the desired architectural pattern for new features that might involve both server-rendered initial views and client-side interactivity?

## Next Steps
1.  **Static Analysis for Unused Astro Files:**
    *   *Action*: Systematically review files in `frontend/src/pages/` and `frontend/src/layouts/`. Use project search tools or manual inspection to identify Astro files with no clear incoming links or references from routing or other essential components.
    *   *Rationale*: To identify and confirm truly unused Astro templates and layouts.
    *   *Logging/Debugging*: Mark potential candidates; temporarily remove/rename and run build/tests to confirm they are not essential.
2.  **Identify Unused Components (Astro & React):**
    *   *Action*: Use IDE features ("Find Usages") or linters (e.g., ESLint with relevant plugins) to scan `frontend/src/components/` for both `.astro` and `.tsx` components that are not imported or utilized by any active page or other component.
    *   *Rationale*: To remove orphaned UI components.
    *   *Logging/Debugging*: Comment out suspected unused components and their imports. Run application and test suites to ensure no functionality is broken.
3.  **Map and Refine SSR-to-CSR Data Flow:**
    *   *Action*: For pages integrating Astro and React (e.g., using `client:load`, `client:idle`), document how props are passed and how state is initialized in React components. Identify inconsistencies or overly complex patterns.
    *   *Rationale*: To streamline the data handoff between server-rendered content and client-side hydrated components, addressing the "clean up interaction" goal.
    *   *Logging/Debugging*: Use browser developer tools and `console.log` statements in Astro page scripts and React component lifecycle methods/hooks (`useEffect`) to trace data passage and component initialization.
4.  **Audit API Client Usage in `frontend/src/lib/`:**
    *   *Action*: For each function in the API client module(s) within `frontend/src/lib/`, use "Find Usages" to trace where it's called. Identify functions with no usages.
    *   *Rationale*: To find and remove dead code related to backend API interactions.
    *   *Logging/Debugging*: Comment out suspected unused API client functions. Thoroughly test frontend features that might have relied on them.
5.  **Review Backend Endpoints (Conditional):**
    *   *Action*: If Step 4 identifies unused frontend API client functions, list the corresponding backend API endpoints. Investigate server logs (if available) or temporarily add specific logging to these endpoints in `backend/app/api/` to check for any incoming requests.
    *   *Rationale*: To identify and potentially deprecate unused backend API endpoints, ensuring a full cleanup.
    *   *Logging/Debugging*: Monitor server logs for calls to suspected orphaned endpoints over a reasonable period.
6.  **Incremental Refactoring and Removal:**
    *   *Action*: Based on findings from Steps 1-5, create small, focused pull requests to remove confirmed dead code and refactor identified SSR/CSR interaction points or API calls.
    *   *Rationale*: To make changes manageable, easier to review, and reduce the risk of regressions.
    *   *Logging/Debugging*: Rely heavily on existing automated tests (`Vitest`, `Playwright`, `pytest`). Manually verify affected user flows after each significant change.
7.  **Update Documentation:**
    *   *Action*: If architectural patterns for SSR/CSR interaction or API usage are clarified or changed, update relevant project documentation (e.g., READMEs, `shared.mdc`, or any developer guides).
    *   *Rationale*: To ensure the team is aligned on the cleaned-up architecture and to prevent future accumulation of similar issues.

## Additional Notes
- Prioritize changes that remove code over complex refactors, unless a refactor directly enables significant code removal or fixes a known bug.
- Communicate with Marysia Lowas-Rzechonek throughout the process, especially when confirming the utility of ambiguous code sections or discussing refactoring approaches for SSR/CSR interactions.
- Ensure all changes are covered by existing tests or that new tests are added if necessary, particularly for refactored interaction points. 