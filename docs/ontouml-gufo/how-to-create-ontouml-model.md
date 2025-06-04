# How to Create an OntoUML Model

Creating an OntoUML model requires a modeling tool that supports UML class diagrams. Since an OntoUML model is a valid UML class diagram enriched with specific stereotypes, it can, in principle, be created using any standard UML modeling tool that allows users to define custom stereotypes.

The recommended approach is to use [**Visual Paradigm**](https://www.visual-paradigm.com), a widely adopted UML modeling environment that integrates well with the OntoUML ecosystem through the [**ontouml-vp-plugin**](https://w3id.org/ontouml/vp-plugin). This plugin provides native support for OntoUML stereotypes, model validation, and export to machine-readable formats.

Other UML tools can also be used to manually create OntoUML models. Since OntoUML models conform to UML class diagram syntax, you can use any modeling environment that allows the definition of custom stereotypes or tags. Examples include:

- [Astah UML](https://astah.net/products/uml/) – Lightweight UML modeling with custom profile support.
- [Enterprise Architect (EA)](https://sparxsystems.com/products/ea/) – Robust, professional-grade tool supporting UML profiles and custom stereotypes.
- [StarUML](https://staruml.io) – Cross-platform tool with extensibility through plugins.
- [Modelio](https://www.modelio.org) – Free and open-source UML/BPMN tool with profile extension support.
- [Papyrus](https://www.eclipse.org/papyrus/) – Open-source, Eclipse-based UML modeling framework with support for custom profiles.

When using these tools, OntoUML stereotypes (e.g., `«kind»`, `«role»`, `«relator»`) must be applied manually, and modelers must follow the conceptual modeling guidelines provided by the Unified Foundational Ontology (UFO).

## Installation Guide for Visual Paradigm and the OntoUML Plugin

The following steps describe how to set up a modeling environment using Visual Paradigm and the `ontouml-vp-plugin`.

### Step 1: Install Visual Paradigm

Visual Paradigm is a commercial UML tool, but it offers a **Community Edition** that is free for non-commercial use.

- **Download Visual Paradigm**: [https://www.visual-paradigm.com/download/](https://www.visual-paradigm.com/download/)
- **Community Edition**: [https://www.visual-paradigm.com/download/community.jsp](https://www.visual-paradigm.com/download/community.jsp)

Follow the installation instructions for your operating system (Windows, macOS, or Linux).

### Step 2: Install the OntoUML Plugin

To enable native support for OntoUML, you’ll need to install the open-source plugin:

#### 2.1 Download the Plugin

- GitHub repository: [https://github.com/OntoUML/ontouml-vp-plugin](https://github.com/OntoUML/ontouml-vp-plugin)
- Latest release (`.zip` file): [https://github.com/OntoUML/ontouml-vp-plugin/releases](https://github.com/OntoUML/ontouml-vp-plugin/releases)

Download the most recent `zip` file compatible with your Visual Paradigm version.

#### 2.2 Install the Plugin in Visual Paradigm

1. Open Visual Paradigm.
2. Navigate to **Help → Install Plugin**.
3. Select the `.zip` file you downloaded.
4. Restart Visual Paradigm when prompted.

### Step 3: Create an OntoUML Diagram

After installation:

1. Go to **Modeling → New Diagram**.
2. Choose **OntoUML Class Diagram**.
3. Use the OntoUML palette to add semantically grounded elements like:
   - `Kind`, `Quantity`, `Collective`, `SubKind`
   - `Role`, `Phase`, `Category`, `Mixin`
   - `Relator`, `Mode`, `Event`, etc.

These elements reflect ontological distinctions from the Unified Foundational Ontology (UFO).

## Additional Features of the Plugin

The `ontouml-vp-plugin` offers several modeling enhancements:

- **Stereotype-aware modeling**: Palette and toolbox tailored to OntoUML.
- **Model validation**: Built-in verification of OntoUML-specific constraints.
- **Export options**: Support for JSON and RDF serialization via other OntoUML tools.

For more details, see the plugin documentation:  
[https://github.com/OntoUML/ontouml-vp-plugin#readme](https://github.com/OntoUML/ontouml-vp-plugin#readme)