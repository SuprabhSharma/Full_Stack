// React passes the props as an object. Conceptually, it looks like this:
function StudentTable({ students , onDeleteStudent , onEditStudent}) {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Course</th>
          <th>Age</th>
          <th>marks</th>
          <th>Grade</th>
          <th>Delete Student</th>
        </tr>
      </thead>
      <tbody>
        {students.map((student) => (
          <tr key={student.id}>
            <td>{student.id}</td>
            <td>{student.name}</td>
            <td>{student.email}</td>
            <td>{student.course}</td>
            <td>{student.age}</td>
            <td>{student.marks}</td>
            <td>{student.grade}</td>
            <td className="student-actions">
              <button 
              type="button"
              onClick={() => onDeleteStudent(student.id)}
              >
              Delete Student
              </button>
              <button
              type="button"
              onClick={()=> onEditStudent(student)}
              >
                Update
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default StudentTable;
