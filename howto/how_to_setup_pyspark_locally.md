### ✅ How to Set Up PySpark Locally

If you see the error below while running this application:

```
JAVA_HOME is not set. 
PySparkRuntimeError: [JAVA_GATEWAY_EXITED] Java gateway process exited before sending its port number.
```

That means Spark cannot find your Java installation. Spark depends on Java (JDK 8 or 11 recommended) to work, even when running locally.

---

### Step-by-Step Guide:

#### 1. **Install Java (JDK 8 or 11 preferred)**

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install openjdk-11-jdk
  ```

- **macOS (using Homebrew)**:
  ```bash
  brew install openjdk@11
  ```

- **Windows**:
  Download and install from [Adoptium](https://adoptium.net/) or Oracle JDK.

---

#### 2. **Set the `JAVA_HOME` Environment Variable**

- **macOS/Linux**:
  Add to your `~/.bashrc`, `~/.zshrc`, or shell profile:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 11)  # macOS
  # Or manually, for example:
  export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
  export PATH=$JAVA_HOME/bin:$PATH
  ```

- **Windows**:
  - Go to: `Control Panel > System > Environment Variables`
  - Create or update `JAVA_HOME` to point to your JDK root directory, e.g.:
    ```
    C:\Program Files\Java\jdk-11
    ```
  - Add `%JAVA_HOME%\bin` to the `Path` variable.

---

#### 3. **Install PySpark**

Add to your `requirements.txt`:
```
pyspark>=3.5.0
```

Or install manually:
```bash
pip install pyspark>=3.5.0
```

---

#### 4. **Test the Setup**

Create a file called `test_spark.py`:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestSpark").getOrCreate()
df = spark.createDataFrame([{"a": 1}, {"a": 2}])
df.show()
```

Run it:
```bash
python test_spark.py
```

If the setup is correct, you'll see output like:

```
+---+
|  a|
+---+
|  1|
|  2|
+---+
```


