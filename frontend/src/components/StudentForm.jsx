import { useState, useEffect } from "react";

function StudentForm({ onAddStudent, student, onUpdateStudent, onCancel }) {
  const isEditing = Boolean(student);
  const [formData, setFormData] = useState({
    // setfromdata by defautl has an an callback
    id: student?.id || "",
    name: student?.name || "",
    age: student?.age || "",
    email: student?.email || "",
    course: student?.course || "",
    marks: student?.marks || "",
  });

  useEffect(() => {
    if (student) {
      setFormData({
        id: student.id || "",
        name: student.name || "",
        age: student.age || "",
        email: student.email || "",
        course: student.course || "",
        marks: student.marks || "",
      });
    }
  }, [student]);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    const changes = {
      name: formData.name,
      age: Number(formData.age),
      email: formData.email,
      course: formData.course,
      marks: Number(formData.marks),
    };

    if (isEditing) {
      onUpdateStudent(student.id, changes);
    } else {
      onAddStudent({
        ...formData,
        age: Number(formData.age),
        marks: Number(formData.marks),
      });
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>{isEditing ? "Update Student" : "Add new Student"}</h2>
      <input
        name="id"
        placeholder="Student ID"
        value={formData.id}
        onChange={handleChange}
        required
        readOnly={isEditing}
      />
      <input
        name="name"
        placeholder="Student Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <input
        name="age"
        placeholder="Student Age"
        type="number"
        value={formData.age}
        onChange={handleChange}
        required
      />
      <input
        name="email"
        type="email"
        placeholder="Student Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        name="course"
        placeholder="Student Course"
        value={formData.course}
        onChange={handleChange}
        required
      />
      <input
        name="marks"
        placeholder="Student Marks"
        type="number"
        value={formData.marks}
        onChange={handleChange}
        required
      />
      <button type="submit">{isEditing ? "Update Student" : "Submit"}</button>

      {isEditing && (
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      )}
    </form>
  );
}

export default StudentForm;
