# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Upload Login Dashboard Bugs
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bugs exist
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bugs exist
  - **Scoped PBT Approach**: For deterministic bugs, scope the property to the concrete failing case(s) to ensure reproducibility
  - Test implementation details from Bug Condition in design:
    - Upload form submission with valid PDF/URL returns "Please select an input method" error
    - Login form with valid credentials fails authentication or shows validation errors
    - Password reset request with valid email fails to send OTP
    - Dashboard access shows dark theme instead of light theme
    - Upload page missing bulk upload functionality (only 2 tabs instead of 3)
    - Navbar logo icon changed from original design (now shows fa-brain)
    - Contact page uses custom blue theme instead of global theme consistency
    - Login form field names don't match EmailLoginForm (username vs email)
    - Login page missing show password toggle and proper error display
    - Login page logo text has CSS rendering issues
  - The test assertions should match the Expected Behavior Properties from design
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bugs exist)
  - Document counterexamples found to understand root cause
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Core Functionality Preservation
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy inputs:
    - Successful PDF uploads and analysis workflows
    - Successful URL scraping and analysis
    - Working export functionality (PDF, TXT, JSON, CSV)
    - Proper navigation and UI interactions
    - Authentication for protected pages
    - Library and compare papers features
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 3. Fix for upload, login, and dashboard issues

  - [x] 3.1 Restore bulk upload functionality to upload page
    - Add missing "Bulk Upload" tab to upload.html template
    - Create corresponding panel with file input for multiple PDFs
    - Update switchTab() JavaScript function to handle 'bulk' input type
    - Ensure proper tab switching and input_type field synchronization
    - _Bug_Condition: isBugCondition(input) where input.action = "upload_form_submit"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 1_
    - _Preservation: Core analysis functionality from design Property 5_
    - _Requirements: 2.1_

  - [x] 3.2 Fix upload form validation and input_type handling
    - Fix input_type hidden field synchronization in upload.html
    - Enhance form validation in analyze_document view
    - Add explicit validation for input_type parameter
    - Provide clearer error messages for missing or invalid input types
    - Add logging for debugging form submission issues
    - _Bug_Condition: isBugCondition(input) where input.input_type IN ['pdf', 'url']_
    - _Expected_Behavior: expectedBehavior(result) from design Property 1_
    - _Preservation: PDF and URL analysis workflows from design Property 5_
    - _Requirements: 2.2, 2.3_

  - [x] 3.3 Add bulk upload processing support
    - Extend analyze_document view to handle multiple file uploads
    - Add batch processing logic for bulk analysis
    - Implement proper response handling for bulk operations
    - Ensure bulk upload integrates with existing analysis pipeline
    - _Bug_Condition: isBugCondition(input) where input.action = "bulk_upload"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 1_
    - _Preservation: Single file analysis workflows from design Property 5_
    - _Requirements: 2.1_

  - [x] 3.4 Fix login authentication and form processing
    - Fix form field name mismatch: change name="username" to name="email" in login.html
    - Add proper error display for form.email.errors and form.password.errors
    - Add "show password" toggle button with JavaScript functionality
    - Fix CSS rendering issues with brand logo text and z-index problems
    - Ensure form data is properly passed to EmailLoginForm
    - Add clear success/failure feedback for login attempts
    - Test login flow with both valid and invalid credentials
    - _Bug_Condition: isBugCondition(input) where input.action = "login_submit"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 2_
    - _Preservation: Authentication for protected pages from design Property 5_
    - _Requirements: 2.4, 2.5, 2.6, 2.7, 2.8_

  - [x] 3.5 Fix password reset OTP flow
    - Improve OTP email sending in otp_utils.py
    - Add timeout configuration for email sending
    - Implement retry logic for failed email delivery
    - Add better logging and error reporting for email issues
    - Test password reset flow end-to-end
    - _Bug_Condition: isBugCondition(input) where input.action = "password_reset_request"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 3_
    - _Preservation: Existing user management features from design Property 5_
    - _Requirements: 2.5_

  - [x] 3.6 Fix dashboard theme consistency
    - Remove dark mode media queries from dashboard.html template
    - Ensure dashboard styling is consistent with global light theme
    - Test theme consistency across different screen sizes
    - Verify no CSS conflicts with other pages
    - _Bug_Condition: isBugCondition(input) where input.action = "dashboard_access"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 4_
    - _Preservation: Navigation and UI elements from design Property 5_
    - _Requirements: 2.6_

  - [x] 3.7 Fix navbar branding consistency
    - Restore original navbar logo icon (if different from fa-brain)
    - Ensure navbar brand colors match the original design
    - Verify navbar styling is consistent across all pages
    - Test navbar responsiveness and mobile display
    - _Bug_Condition: isBugCondition(input) where input.page = "navbar"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 6_
    - _Preservation: Navigation functionality from design Property 5_
    - _Requirements: 2.7_

  - [x] 3.8 Fix contact page theme consistency
    - Remove custom CSS variables (--contact-primary, --contact-secondary) from contact.html
    - Replace custom blue theme with global application theme
    - Ensure contact page styling matches rest of application
    - Test contact page across different screen sizes
    - Verify form functionality still works after theme changes
    - _Bug_Condition: isBugCondition(input) where input.page = "contact"_
    - _Expected_Behavior: expectedBehavior(result) from design Property 7_
    - _Preservation: Contact form functionality from design Property 5_
    - _Requirements: 2.8_

  - [x] 3.9 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Upload Login Dashboard Fixes
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bugs are fixed)
    - _Requirements: Expected Behavior Properties from design_

  - [x] 3.10 Verify preservation tests still pass
    - **Property 2: Preservation** - Core Functionality Preservation
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.