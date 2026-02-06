# Yama Story Script Structural Rules (Physically Enforced)

## 1. The "Golden Ratio" (1:7:2)
All scripts MUST adhere to the following character count distribution:

| Section | Role | Target Ratio | Tolerance |
| :--- | :--- | :--- | :--- |
| **起 (Ki)** | Introduction / Hook | **10%** | ±5% (5-15%) |
| **承 (Sho)** | The Incident / **Human Action** | **70%** | ±10% (60-80%) |
| **転結 (Ten-Ketsu)** | Conclusion / Lesson | **20%** | ±5% (15-25%) |

## 2. Mandatory Markers
Scripts must explicitly demarcate these sections using HTML comments to allow the Validator to parse them physically.

```markdown
<!-- PART: KI -->
## 1. Introduction...

<!-- PART: SHO -->
## 2. The incident...

<!-- PART: TEN-KETSU -->
## 11. Conclusion...
```

## 3. Action Density (The "System 2" Check)
The **承 (Sho)** section must focus on "Human Action", not just explanation.
The Validator checks for "Visual/Action Keywords" in the production notes (Col E equivalent / AI Video Prompts) of this section.

## 4. Validator Execution
Before any script is presented to the user, you MUST run:
`python3 Yama_Story/System_Tools/validate_yama_structure.py <script_path>`
