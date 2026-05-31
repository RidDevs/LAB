const loadData = () => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve([
                { name: "John", marks: 80 },
                { name: "Alice", marks: 90 }
            ]);
        }, 1000);
    });
};

const processData = (data) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(
                data.map(student => ({
                    ...student,
                    status: student.marks >= 50 ? "Pass" : "Fail"
                }))
            );
        }, 1000);
    });
};

const displayData = (data) => {
    console.log(data);
};

const main = async () => {
    const data = await loadData();
    const processed = await processData(data);
    displayData(processed);
};

main();