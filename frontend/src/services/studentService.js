const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getStudents = async (page = 1, limit = 16) => {
  try {
    // Build query parameters
    const params = new URLSearchParams({
      page: String(page),
      limit: String(limit),
    });

    // Send a get request

    const response = await fetch(`${API_BASE_URL}/students?${params}`);

    // Parse the response

    const data = await response.json().catch(() => null);

    // Check the http request
    if (!response.ok) {
      throw new Error(data?.detail || `Request Failed : ${response.status}`);
    }

    return data;
  } catch (error) {
    // handle and propogate error
    console.error("Error fetching students ", error.message); // displays the error in the browser

    throw error; // propogates the error back tothe component that called getStudents()
  }
};

export const addStudent = async (student) => {
  try {
    const response = await fetch(`${API_BASE_URL}/student`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(student),
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(
        data?.detail || `Request Failed with status ${response.status}`,
      );
    }
    return data;
  } catch (error) {
    console.error("Could not add STudent :", error);
    throw error;
  }
};

export const deleteStudent = async (studenID) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/student/${encodeURIComponent(studenID)}`,
      {
        method: "DELETE",
      },
    );
    const data = await response.json().catch(() => null);

    // Check the http response
    if (!response.ok) {
      throw new Error(
        data?.detail || `Request failed with status ${response.status}`,
      );
    }
    return data;
  } catch (error) {
    console.error("Could not delte the student :", error);

    throw error;
  }
};

export const getStudentById = async (studentId) => {
  const response = await fetch(
    `${API_BASE_URL}/student/${encodeURIComponent(studentId)}`,
  );
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || `Request failed with status ${response.status}`,
    );
  }

  return data;
};

export const updateStudent = async (studentID, student) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/update_student/${encodeURIComponent(studentID)}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(student),
      },
    );
    const data = await response.json().catch(() => null);

    if (!response.ok) {
        throw new Error (
            data?.detail || `Reques failed with status ${response.status}`
        )
    }
    return data ;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
