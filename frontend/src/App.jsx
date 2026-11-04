import { useEffect, useState } from "react";
import {
  addStudent,
  getStudents,
  deleteStudent,
  updateStudent,
  getStudentById,
} from "./services/studentService";
import StudentTable from "./components/StudentTable";
import StudentForm from "./components/StudentForm";

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editingStudent, setEditingStudent] = useState(null);
  const [searchId, setSearchId] = useState("");
  const [searchedStudent, setSearchedStudent] = useState(null);

  const loadStudent = async () => {
    try {
      setLoading(true);
      setError("");

      const studentList = await getStudents();
      setStudents(studentList.students);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGetStudentById = async (event) => {
    event.preventDefault();

    try {
      setError("");
      setSearchedStudent(null);

      const student = await getStudentById(searchId.trim());
      setSearchedStudent(student);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleShowAllStudents = () => {
    setError("");
    setSearchId("");
    setSearchedStudent(null);
  };

  const handleUpdateStudent = async (studentId, changes) => {
    try {
      setError("");

      const updatedStudent = await updateStudent(studentId, changes);

      setStudents((currentStudents) =>
        currentStudents.map((student) =>
          student.id === studentId ? { ...student, ...updatedStudent } : student,
        ),
      );
      setEditingStudent(null);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleDeleteStudent = async (studentId) => {
    try {
      setError("");

      await deleteStudent(studentId);

      setStudents((currentStudents) =>
        currentStudents.filter((student) => student.id !== studentId),
      );
    } catch (error) {
      setError(error.message);
    }
  };

  const handleAddStudents = async (student) => {
    try {
      setError("");

      const newStudent = await addStudent(student);

      setStudents((prevStudent) => [...prevStudent, newStudent]);
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    loadStudent();
  }, []);

  return (
    <main>
      <h1 style={{ textAlign: "center" }}>Student Management</h1>

      <StudentForm
        student={editingStudent}
        onAddStudent={handleAddStudents}
        onUpdateStudent={handleUpdateStudent}
        onCancel={() => setEditingStudent(null)}
      />
      <form onSubmit={handleGetStudentById}>
        <h2>Find Students</h2>

        <input
          type="text"
          placeholder="Enter the Student ID"
          value={searchId}
          onChange={(event) => setSearchId(event.target.value)}
          required
        />
        <button type="submit"> Get Student</button>
        <button type="button" onClick={handleShowAllStudents}>
          See All Students
        </button>
      </form>

      {loading && <p> Loading students </p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <>
          <h2>Total Students : {students.length}</h2>
          <StudentTable
            students={searchedStudent ? [searchedStudent] : students}
            onDeleteStudent={handleDeleteStudent}
            onEditStudent={setEditingStudent}
          />
        </>
      )}
    </main>
  );
}

export default App;

// This passes props from App.jsx to the StudentTable component.

// StudentTable — React component being rendered.
// students — prop name.
// {students} — value passed to the prop. It is the students state array from App.jsx.
// onDeleteStudent — prop name.
// {handleDeleteStudent} — function passed to the component.
