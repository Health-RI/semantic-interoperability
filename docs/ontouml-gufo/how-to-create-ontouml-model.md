# How to Create an OntoUML Model

Creating an OntoUML model requires a modeling tool that supports UML diagrams and can be extended with OntoUML-specific semantics. The recommended approach is to use **Visual Paradigm**, a widely adopted UML modeling environment that integrates well with the OntoUML ecosystem through the **ontouml-vp-plugin**.

## Step 1: Install Visual Paradigm

Visual Paradigm is a commercial modeling tool, but it offers a **Community Edition** that is free for non-commercial use, such as academic and personal projects.

- **Download Visual Paradigm**: [https://www.visual-paradigm.com/download/](https://www.visual-paradigm.com/download/)
- **More about the free Community Edition**: [https://www.visual-paradigm.com/download/community.jsp](https://www.visual-paradigm.com/download/community.jsp)

Once downloaded, follow the standard installation process for your operating system (Windows, macOS, or Linux).

## Step 2: Install the OntoUML Plugin for Visual Paradigm

To enable OntoUML-specific modeling capabilities, you need to install the **ontouml-vp-plugin**, which extends Visual Paradigm by introducing OntoUML stereotypes, a dedicated diagram type, and validation features.

### 2.1 Download the Plugin

The plugin is open-source and publicly available on GitHub:

- **GitHub Repository**: [https://github.com/OntoUML/ontouml-vp-plugin](https://github.com/OntoUML/ontouml-vp-plugin)
- **Releases page (download the `.vpplugin` file)**: [https://github.com/OntoUML/ontouml-vp-plugin/releases](https://github.com/OntoUML/ontouml-vp-plugin/releases)

Always download the most recent release for compatibility with newer versions of Visual Paradigm.

### 2.2 Install the Plugin

To install the plugin:

1. Open Visual Paradigm.
2. Go to **Tools → Plugins → Install Plugin**.
3. Select the downloaded `.vpplugin` file.
4. Visual Paradigm will ask you to restart to activate the plugin.

After restarting, you will see the OntoUML extension listed among your installed plugins.

## Step 3: Create an OntoUML Diagram

After installation:

1. Go to **Modeling → New Diagram**.
2. Select **OntoUML Class Diagram** (provided by the plugin).
3. You’ll see a new palette with OntoUML-specific modeling elements like:
   - `Kind`, `Quantity`, `Collective`, `SubKind`
   - `Role`, `Phase`, `Category`, `Mixin`
   - `Relator`, `Event`, `Mode`, and others

These elements are semantically grounded in the **Unified Foundational Ontology (UFO)** and support ontology-driven conceptual modeling.

## Additional Features

The `ontouml-vp-plugin` also includes:

- **Model validation**: Check whether your model satisfies syntactic constraints of OntoUML.
- **Semantic guidance**: Tooltips and palette icons help clarify the purpose of each stereotype.
- **Export options**: OntoUML models can be exported for processing or conversion into JSON or RDF using complementary tools.

For more details, refer to the official documentation on GitHub:  
[https://github.com/OntoUML/ontouml-vp-plugin#readme](https://github.com/OntoUML/ontouml-vp-plugin#readme)

---

By following these steps, you will have a fully functional environment for developing OntoUML models in a graphical and semantically rich way. This setup is ideal for students, researchers, and practitioners working on ontology-driven conceptual modeling.